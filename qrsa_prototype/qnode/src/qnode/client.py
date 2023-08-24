import socket
import uuid
import requests
import ipaddress
from fastapi import Depends
from typing import Union, List
from ipaddress import IPv4Address, IPv6Address
from dependency_injector.wiring import inject, Provide

from common.models.connection_setup_request import ConnectionSetupRequest
from common.models.app_performance_requirement import ApplicationPerformanceRequirement

from qnode.containers import Container
from qnode.connection_manager.connection_manager import ConnectionManager
from qnode.hardware_monitor.hardware_monitor import HardwareMonitor
from qnode.routing_daemon.routing_daemon import RoutingDaemon

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


class QRSAClient:
    """
    Initiate connection setup process
    """

    def __init__(self):
        self.pending_connection: List[str] = []

    # Application will use this function to start entire connection setup process
    @inject
    def send_connection_setup_request(
        self,
        destination: Union[IPv4Address, IPv6Address],
        application_perofrmance_request: ApplicationPerformanceRequirement,
        connection_manager: ConnectionManager = Provide[Container.connection_manager],
        hardware_monitor: HardwareMonitor = Provide[Container.hardware_monitor],
        routing_daemon: RoutingDaemon = Provide[Container.routing_daemon],
    ):
        # Generate random application id
        application_id = str(uuid.uuid4())
        # Get the latest hardware perofrmance indicator
        performance_indicator = hardware_monitor.get_performance_indicator()
        # Create connection setup request
        csr_contents = {
            "header": {
                "src": ipaddress.ip_address(ip_address),
                "dst": destination,
            },
            "application_id": application_id,
            "app_performance_requirement": application_perofrmance_request,
            "performance_indicators": {ip_address: performance_indicator},
            "host_list": [ip_address],
        }

        csr = ConnectionSetupRequest(**csr_contents)

        # TODO: Get next hop from routing table
        next_hop = routing_daemon.get_next_hop(destination)
        # Serialize connection setup request
        csr_json = csr.model_dump_json()
        requests.post(
            f"http://{next_hop}:8080/connection_setup_request",
            data=csr_json,
            headers={"Content-Type": "application/json"},
        )
