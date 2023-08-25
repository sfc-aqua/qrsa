import uuid
import aiohttp
import asyncio
from typing import Tuple, List, Dict, Any
from dependency_injector.providers import Configuration

from common.models.ruleset import RuleSet
from common.models.connection_setup_request import ConnectionSetupRequest
from common.models.connection_setup_response import ConnectionSetupResponse
from common.models.performance_indicator import PerformanceIndicator
from common.models.link_allocation_update import LinkAllocationUpdate
from common.models.connection import ConnectionMeta
from common.models.barrier import Barrier
from common.models.app_performance_requirement import ApplicationPerformanceRequirement
from common.type_utils import IpAddressType
from common.log.logger import logger

from qnode.connection_manager.ruleset_factory import RuleSetFactory
from qnode.connection_manager.interface import AbstractConnectionManager


class ConnectionManager(AbstractConnectionManager):
    def __init__(self, config: Configuration):
        """
        Constructor for ConnectionManager

        config is set in Container.
        """
        self.config = config
        self.ruleset_factory = RuleSetFactory()
        # application_id -> connection_id
        self.application_id_to_connection_id: Dict[str, str] = {}
        # application_id -> ConnectionMeta
        self.pending_connections: Dict[str, ConnectionMeta] = {}
        # connection_id -> ConnectionMeta
        self.running_connections: Dict[str, ConnectionMeta] = {}
        # neighbor address -> lau
        self.sent_la: Dict[IpAddressType, LinkAllocationUpdate] = {}

    async def send_connection_setup_request(
        self,
        destination: IpAddressType,
        next_hop: IpAddressType,
        application_performance_requirement: ApplicationPerformanceRequirement,
        performance_indicator: PerformanceIndicator,
    ):
        """
        Send connection setup request to the next hop
        This function can only be called in the initiator node
        """
        # Generate random application id to map application
        # and connection_id given by responder
        application_id = str(uuid.uuid4())

        # Create connection setup request
        csr_json = ConnectionSetupRequest(
            **{
                "header": {
                    "src": self.config["meta"]["ip_address"],
                    "dst": destination,
                },
                "application_id": application_id,
                "app_performance_requirement": application_performance_requirement,
                "performance_indicators": {
                    self.config["meta"]["ip_address"]: performance_indicator
                },
                "host_list": [self.config["meta"]["ip_address"]],
            }
        ).model_dump_json()

        self.pending_connections[application_id] = ConnectionMeta(
            **{
                "prev_hop": None,
                "next_hop": next_hop,
                "source": self.config["meta"]["ip_address"],
                "destination": destination,
            }
        )

        # Send request to next hop
        response, status_code = await self.send_message(
            csr_json, next_hop, "connection_setup_request"
        )
        return response

    async def respond_to_connection_setup_request(
        self,
        given_request: ConnectionSetupRequest,
        performance_indicator: PerformanceIndicator,
    ) -> (str, RuleSet):
        """
        Respond to a connection setup request.
        This function creates and distributes RuleSets to intermediate nodes.

        A ruleset for this responder node is returned here.

        Arguments:
            given_request: ConnectionSetupRequest that is received at the responder node
            performance_indicator: PerformanceIndicator of this node

        Returns:
            str: Connection id for this RuleSet
            RuleSet: A ruleset for this responder node
        """

        # Get my ip address
        ip_address = self.config["meta"]["ip_address"]

        # create connection meta and register it to running connections
        connection_meta = ConnectionMeta(
            # at the end of host list, there should be the previous hop informaion
            prev_hop=given_request.host_list[-1],
            next_hop=None,  # This should be responder, so next hop is None
            source=given_request.header.src,
            destination=given_request.header.dst,
        )

        # create connection id
        connection_id = str(uuid.uuid4())
        self.running_connections[connection_id] = connection_meta

        # Append this node's information to the given request
        given_request.host_list.append(ip_address)
        given_request.performance_indicators |= {ip_address: performance_indicator}

        # create ruleset
        rulesets = self.ruleset_factory.create_ruleset(
            connection_id,
            host_lists=given_request.host_list,
            performance_indicators=given_request.performance_indicators,
        )

        self_ruleset = None
        # send rulesets to intermediate nodes
        for host in given_request.host_list:
            if host == ip_address:
                # The last ruleset goes to this node itself.
                # This doesn't have to be sent to other nodes.
                self_ruleset = rulesets[host]
            else:
                logger.debug(f"Sending RuleSet to {host}")
                # Take a ruleset and send it to destination
                connection_setup_response_json = ConnectionSetupResponse(
                    **{
                        "application_id": given_request.application_id,
                        "connection_id": connection_id,
                        "ruleset": rulesets[host],
                    }
                ).model_dump_json()

                # Send message in json format
                response, status_code = await self.send_message(
                    connection_setup_response_json,
                    host,
                    "connection_setup_response",
                )
                logger.debug(f"Sent RuleSet to {host}")
        return (connection_id, self_ruleset)

    async def forward_connection_setup_request(
        self,
        given_request: ConnectionSetupRequest,
        performance_indicator: PerformanceIndicator,
        next_hop: IpAddressType,
    ):
        """
        Forward a received connection setup to next hop
        """
        # Store information about this connection
        connection_meta = ConnectionMeta(
            prev_hop=given_request.host_list[-1],
            next_hop=next_hop,
            source=given_request.header.src,
            destination=given_request.header.dst,
        )

        # When the connection setup response is received,
        # this connection meta will be moved to running connections
        self.pending_connections[given_request.application_id] = connection_meta

        # Append this node's performance indicator to the request
        given_request.performance_indicators |= {
            self.config["meta"]["ip_address"]: performance_indicator
        }

        # Create a new request based  on forward request
        app_req = given_request.app_performance_requirement
        given_request.host_list.append(self.config["meta"]["ip_address"])

        new_request_json = ConnectionSetupRequest(
            **{
                "header": given_request.header,
                "application_id": given_request.application_id,
                "app_performance_requirement": app_req,
                "performance_indicators": given_request.performance_indicators,
                "host_list": given_request.host_list,
            }
        ).model_dump_json()

        # Send request to next hop
        response, status_code = await self.send_message(
            new_request_json, next_hop, "connection_setup_request"
        )
        return response

    def update_pending_connection_to_running_connection(
        self, connection_id: str, application_id: str
    ):
        if self.pending_connections.get(application_id) is None:
            raise Exception(
                f"Application id {application_id} is not in pending connections"
            )
        else:
            self.running_connections[connection_id] = self.pending_connections[
                application_id
            ]

    async def send_lau_update(
        self, neighbors: List[IpAddressType], proposed_la: LinkAllocationUpdate
    ):
        """
        Send LAU update to the neighbor nodes
        """
        # If this node has larger ip address
        # than the neighbor's ip address,send lau update
        tasks = [
            self.send_message(
                proposed_la.model_dump_json(), neighbor, "link_allocation_update"
            )
            for neighbor in neighbors
            if self.config["meta"]["ip_address"] > neighbor
        ]
        results = await asyncio.gather(*tasks)
        logger.debug(
            f"Sent LAU update to {[nb for nb in neighbors if self.config['meta']['ip_address'] > nb]} from {self.config['meta']['hostname']}"  # noqa
        )
        return results

    async def send_barrier(
        self,
        connection_id: str,
        neighbors: List[IpAddressType],
        target_pptsns: Dict[IpAddressType, int],
    ) -> Dict[IpAddressType, int]:
        tasks = [
            self.send_message(
                Barrier(
                    **{
                        "header": {
                            "src": self.config["meta"]["ip_address"],
                            "dst": neighbor,
                        },
                        "connection_id": connection_id,
                        "target_pptsn": target_pptsns[neighbor],
                    }
                ).model_dump_json(),
                neighbor,
                "barrier",
            )
            for neighbor in neighbors
            if self.config["meta"]["ip_address"] > neighbor
        ]
        results = await asyncio.gather(*tasks)
        logger.debug(
            f"Sent barrier message to {[nb for nb in neighbors if self.config['meta']['ip_address'] > nb]} from {self.config['meta']['hostname']}"  # noqa
        )
        return results

    async def send_barrier_response(
        self,
        connection_id: str,
        neighbor: IpAddressType,
        agreed_pptsn: int,
    ):
        """
        A node who received barrier message will send barrier response with agreed pptsn
        """
        barrier = Barrier(
            **{
                "header": {
                    "src": self.config["meta"]["ip_address"],
                    "dst": neighbor,
                },
                "connection_id": connection_id,
                "target_pptsn": agreed_pptsn,
            }
        )
        response, _ = await self.send_message(
            barrier.model_dump_json(), neighbor, "barrier_response"
        )
        return response

    async def send_message(
        self,
        message: Any,
        destination: IpAddressType,
        endpoint: str,
        headers: Dict[str, str] = {"Content-Type": "application/json"},
        port: int = 8080,  # tempral
    ) -> Tuple[str, int]:
        """
        Send a message to a destination
        message needs to implement model_dump_json()
        """
        try:
            url = f"http://{destination}:{port}/{endpoint}"
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    data=message,
                    headers=headers,
                ) as response:
                    resp = await response.read()
                    return (resp, response.status)
        except Exception as e:
            raise e
