import socket
import requests
from typing import Union, Dict
from ipaddress import IPv4Address, IPv6Address
from dependency_injector.providers import Configuration

from common.models.ruleset import RuleSet
from common.models.connection_setup_request import ConnectionSetupRequest
from common.models.performance_indicator import PerformanceIndicator
from common.models.connection import ConnectionMeta
from .ruleset_factory import RuleSetFactory

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


class ConnectionManager:
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
        self, request: ConnectionSetupRequest
    ) -> RuleSet:
        """
        Respond to a connection setup request.
        This function distributes RuleSets to intermediate nodes.

        A ruleset for this responder node is returned here.
        """
        # Connection id is filled when the connection setup response is received
        self.running_connections[request.application_id] = None
        print(self.running_connections)
        return {"test": "test"}

    def link_connection_id_to_application_id(
        self, application_id: str, connection_id: str
    ):
        """
        Link a connection id to an application id
        """
        if application_id not in self.running_connections:
            raise ValueError(f"Application id {application_id} not found")
        self.running_connection[application_id] = connection_id

    async def forward_connection_setup_request(
        self,
        given_request: ConnectionSetupRequest,
        performance_indicator: PerformanceIndicator,
        next_hop: Union[IPv4Address, IPv6Address],
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
        new_request_json = ConnectionSetupRequest(**{
            "header": given_request.header,
            "appliaction_id": given_request.application_id,
            "app_performance_requirement": given_request.app_performance_requirement,
            "performance_indicator": given_request.performance_indicator,
            "hosts": given_request.hosts.append(ip_address),
        }).model_dump_json()

        # Send request to next hop
        requests.post(
            f"https://{next_hop}:8080/connection_setup_request",
            data=new_request_json,
            headers={"Content-Type": "application/json"},
        )
