import socket
import requests
import uuid
from typing import Dict, Any
from dependency_injector.providers import Configuration, Provide

from common.models.ruleset import RuleSet
from common.models.connection_setup_request import ConnectionSetupRequest
from common.models.connection_setup_response import ConnectionSetupResponse
from common.models.performance_indicator import PerformanceIndicator
from common.models.connection import ConnectionMeta
from common.type_utils import IpAddressType

from qnode.connection_manager.ruleset_factory import RuleSetFactory
from qnode.connection_manager.interface import AbstractConnectionManager
from qnode.containers import Container

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


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

    async def respond_to_connection_setup_request(
        self,
        given_request: ConnectionSetupRequest,
        performance_indicator: PerformanceIndicator,
    ) -> RuleSet:
        """
        Respond to a connection setup request.
        This function creates and distributes RuleSets to intermediate nodes.

        A ruleset for this responder node is returned here.
        """
        # Get my ip address
        ip_address = self.config["ip_address"]

        # create connection meta and register it to running connections
        connection_meta = ConnectionMeta(
            # at the end of host list, there should be the previous hop informaion
            prev_hop=given_request.hosts[-1],
            next_hop=None,  # This should be responder, so next hop is None
            source=given_request.header.src,
            destination=given_request.header.dst,
        )

        # create connection id
        connection_id = f"{uuid.uuid4()}"
        self.running_connections[connection_id] = connection_meta

        given_request.hosts.append(ip_address)
        given_request.performance_indicator |= {ip_address: performance_indicator}
        # create ruleset
        rulesets = self.ruleset_factory.create_ruleset(
            connection_id,
            host_lists=given_request.hosts,
            performance_indicators=given_request.performance_indicator,
        )

        # send rulesets to intermediate nodes
        for host in given_request.hosts:
            # Take a ruleset and send it to destination
            connection_setup_response_json = ConnectionSetupResponse(
                **{
                    "application_id": given_request.application_id,
                    "connection_id": connection_id,
                    "ruleset": rulesets,
                }
            ).model_dump_json()

            # Send message in json format
            self.send_message(
                connection_setup_response_json,
                host,
                "connection_setup_response",
            )

            if host == ip_address:
                # The last ruleset goes to this node itself.
                # This doesn't have to be sent to other nodes.
                return rulesets[self.config["ip_address"]]

    def link_connection_id_to_application_id(
        self, application_id: str, connection_id: str
    ):
        """
        Link a connection id to an application id
        """
        if application_id not in self.pending_connections:
            raise ValueError(
                f"Application id {application_id} not found in pending connection"
            )
        # make a map for later use
        self.application_id_to_connection_id[application_id] = connection_id

        # move pending connection to running connection
        self.running_connections[connection_id] = self.pending_connections[
            application_id
        ]

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
            prev_hop=given_request.hosts[-1],
            next_hop=next_hop,
            source=given_request.header.src,
            destination=given_request.header.dst,
        )
        # When this node receives a connection setup response,
        # this connection meta is moved to running connections
        self.pending_connections[given_request.application_id] = connection_meta

        # Append this node's performance indicator to the request
        given_request.performance_indicator |= {
            self.config.ip_address: performance_indicator
        }

        # Create a new request based  on forward request
        app_req = given_request.app_performance_requirement
        new_request_json = ConnectionSetupRequest(
            **{
                "header": given_request.header,
                "appliaction_id": given_request.application_id,
                "app_performance_requirement": app_req,
                "performance_indicator": given_request.performance_indicator,
                "hosts": given_request.hosts.append(ip_address),
            }
        ).model_dump_json()

        # Send request to next hop
        self.send_message(new_request_json, next_hop, "connection_setup_request")

    async def send_message(
        self,
        message: Any,
        destination: IpAddressType,
        endpoint: str,
        headers: Dict[str, str] = {"Content-Type": "application/json"},
        port: int = 8080,  # tempral
        config: Configuration = Provide[Container.config],
    ):
        """
        Send a message to a destination
        message needs to implement model_dump_json()
        """
        try:
            # Serialization format could be configurable
            requests.post(
                f"{destination}:{port}/{endpoint}",
                data=message,
                headers=headers,
            )
        except Exception as e:
            raise e
