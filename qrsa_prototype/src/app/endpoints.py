import socket
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from common.models.connection_setup_request import ConnectionSetupRequest
from common.models.connection_setup_response import ConnectionSetupResponse
from common.models.connection_setup_reject import ConnectionSetupReject

from containers import Container
from connection_manager.connection_manager import ConnectionManager
from hardware_monitor.hardware_monitor import HardwareMonitor
from routing_daemon.routing_daemon import RoutingDaemon


router = APIRouter()

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


@router.get("/heat_beat")
async def heart_beat() -> dict:
    return {"message": "Alive"}


@router.post("/connection_setup_request")
@inject
async def handle_connection_setup_request(
    request: ConnectionSetupRequest,
    connection_manager: ConnectionManager = Depends(
        Provide[Container.connection_manager]
    ),
    hardware_monitor: HardwareMonitor = Depends(Provide[Container.hardware_monitor]),
    routing_daemon: RoutingDaemon = Depends(Provide[Container.routing_daemon]),
) -> dict:
    """
    Experimental function to handle connection setup requests
    :param request: ConnectionSetupRequest
    :return: dict

    In the future, we may want to communicate over a different protocol
    as they are implemented on routers or repeaters.
    """
    if ip_address == request.header.dst:
        # This node is the final destination
        # Create RuleSet
        print(connection_manager, dir(connection_manager))
        await connection_manager.respond_to_connection_setup_request(request)
        return {"message": "Received connection setup request"}

    # The final destination is not this node
    # Forward to next hop
    # Add performance indicator to the request
    performance_indicator = hardware_monitor.get_performance_indicator()
    next_hop_address = routing_daemon.get_next_hop(request.header.dst)
    connection_manager.forward_connection_setup_request(
        request, performance_indicator, next_hop_address
    )
    return {"message": "Received connection setup request"}


@router.post("/connection_setup_response")
async def handle_connection_setup_response(response: ConnectionSetupResponse):
    return {"message": "Received connection setup response"}


@router.post("/connection_setup_reject")
async def handle_connection_setup_reject(reject: ConnectionSetupReject):
    return {"message": "Received connection setup reject"}


@router.post("/lau_update")
async def handle_lau_update():
    return {"message": "Received LAU update"}


@router.post("/barrier")
async def handle_barrier():
    return {"message": "Received barrier"}
