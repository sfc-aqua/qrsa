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
from common.log.logger import logger

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
    async def send_connection_setup_request(
        self,
        destination: Union[IPv4Address, IPv6Address],
        application_performance_requirement: ApplicationPerformanceRequirement,
        connection_manager: ConnectionManager = Provide[Container.connection_manager],
        hardware_monitor: HardwareMonitor = Provide[Container.hardware_monitor],
        routing_daemon: RoutingDaemon = Provide[Container.routing_daemon],
    ):
        logger.debug(f"Start application at {hostname}")
        # Get the latest hardware perofrmance indicator
        performance_indicator = hardware_monitor.get_performance_indicator()

        # TODO: Get next hop from routing table
        next_hop = routing_daemon.get_next_hop(destination)

        await connection_manager.send_connection_setup_request(
            destination,
            next_hop,
            application_performance_requirement,
            performance_indicator,
        )
