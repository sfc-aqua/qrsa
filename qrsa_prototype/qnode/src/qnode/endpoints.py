from typing import Any
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from common.models.connection_setup_request import ConnectionSetupRequest
from common.models.connection_setup_response import ConnectionSetupResponse
from common.models.connection_setup_reject import ConnectionSetupReject
from common.log.logger import logger


from qnode.containers import Container
from qnode.connection_manager.connection_manager import ConnectionManager
from qnode.hardware_monitor.hardware_monitor import HardwareMonitor
from qnode.routing_daemon.routing_daemon import RoutingDaemon
from qnode.rule_engine.rule_engine import RuleEngine

router = APIRouter()


@router.get("/heartbeat")
def heartbeat() -> dict:
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
    rule_engine: RuleEngine = Depends(Provide[Container.rule_engine]),
    config: Any = Depends(Provide[Container.config]),
) -> dict:
    """
    Experimental function to handle connection setup requests
    :param request: ConnectionSetupRequest
    :return: dict

    In the future, we may want to communicate over a different protocol
    as they are implemented on routers or repeaters.
    """
    logger.debug("Received connection setup request")
    if config["ip_address"] == request.header.dst:
        # This node is the final destination
        # Create RuleSet and send back
        # Get my performance indicator
        logger.debug("Connection Setup Request reached to the responder")
        performance_indicator = hardware_monitor.get_performance_indicator()
        responder_ruleset = (
            await connection_manager.respond_to_connection_setup_request(request)
        )
        rule_engine.accept_ruleset(responder_ruleset)
        return {"message": "Received connection setup request"}

    # The final destination is not this node
    # Forward to next hop
    # Add performance indicator to the request
    performance_indicator = hardware_monitor.get_performance_indicator()
    next_hop_address = routing_daemon.get_next_hop(request.header.dst)
    connection_manager.forward_connection_setup_request(
        request, performance_indicator, next_hop_address
    )
    logger.debug("Connection Setup Request forwarded to the next hop")
    return {"message": "Received connection setup request"}


@router.post("/connection_setup_response")
@inject
async def handle_connection_setup_response(
    response: ConnectionSetupResponse,
    connection_manager: ConnectionManager = Depends(
        Provide[Container.connection_manager]
    ),
    rule_engine: RuleEngine = Depends(Provide[Container.rule_engine]),
) -> dict:
    """
    Experimental function to handle connection setup responses
    :param response: ConnectionSetupResponse
    :return: dict
    """
    logger.debug("Received connection setup response")
    # register this connection id to connection manager and tie with application id
    connection_manager.register_connection(
        response.application_id, response.connection_id
    )
    # Get proposed lau from rule engine based on current running ruleset
    proposed_la = rule_engine.accept_ruleset(response)

    connection_manager.send_lau_update(proposed_la)
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
