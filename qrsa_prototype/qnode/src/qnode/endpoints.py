from typing import Any
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from common.models.connection_setup_request import ConnectionSetupRequest
from common.models.connection_setup_response import ConnectionSetupResponse
from common.models.connection_setup_reject import ConnectionSetupReject
from common.models.link_allocation_update import LinkAllocationUpdate
from common.models.application_bootstrap import ApplicationBootstrap
from common.models.barrier import Barrier
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


# Application will use this function to start entire connection setup process
@router.post("/start_connection_setup")
@inject
async def send_connection_setup_request(
    app_bootstrap: ApplicationBootstrap,
    connection_manager: ConnectionManager = Depends(
        Provide[Container.connection_manager]
    ),
    hardware_monitor: HardwareMonitor = Depends(Provide[Container.hardware_monitor]),
    routing_daemon: RoutingDaemon = Depends(Provide[Container.routing_daemon]),
    config: Any = Depends(Provide[Container.config]),
):
    logger.debug(f"Start application at {config['meta']['hostname']}")

    # Get the latest hardware perofrmance indicator
    performance_indicator = hardware_monitor.get_performance_indicator()

    # Get the next hop address from the destination address
    next_hop = routing_daemon.get_next_hop(app_bootstrap.destination)

    # Send connection setup request to the next hop
    response, status_code = await connection_manager.send_connection_setup_request(
        app_bootstrap.destination,
        next_hop,
        app_bootstrap.application_performance_requirement,
        performance_indicator,
    )

    if status_code != 200:
        raise RuntimeError("Connection setup request failed")

    logger.debug(f"Connection setup request sent. response: {response}")

    return JSONResponse(
        content={"message": "Connection setup done"},
        headers={"Content-Type": "application/json"},
    )


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
    if config["meta"]["ip_address"] == request.header.dst:
        # This node is the final destination
        # Create RuleSet and send back
        # Get my performance indicator
        logger.debug("Connection Setup Request reached to the responder")
        performance_indicator = hardware_monitor.get_performance_indicator()

        # Create RuleSet and respond to incoming request
        (
            connection_id,
            responder_ruleset,
        ) = await connection_manager.respond_to_connection_setup_request(
            request, performance_indicator
        )

        # Get proposed lau from rule engine based on current running ruleset
        proposed_lau = rule_engine.accept_ruleset(connection_id, responder_ruleset)

        # Get neighbor information from routing daemon
        neighbors = routing_daemon.get_neighbor_nodes()

        # Send LAU update to the next hop
        await connection_manager.send_link_allocation_update(neighbors, proposed_lau)

        # Get target pptsn with buffer from rule engine
        target_pptsns = rule_engine.get_pptsns_with_buffer(neighbors, 10)

        # Send barrier message
        await connection_manager.send_barrier(connection_id, neighbors, target_pptsns)

        # At this point, the finalized pptsn should be prepared
        finailized_pptsn = rule_engine.get_switching_pptsns(connection_id, neighbors)

        logger.debug(f"Connection setup done. Finalized pptsn: {finailized_pptsn}")

        return JSONResponse(
            content={"message": "Received connection setup request"},
            headers={"Content-Type": "application/json"},
        )

    # The final destination is not this node
    # Forward to next hop
    # Add performance indicator to the request
    performance_indicator = hardware_monitor.get_performance_indicator()
    next_hop_address = routing_daemon.get_next_hop(request.header.dst)
    await connection_manager.forward_connection_setup_request(
        request, performance_indicator, next_hop_address
    )
    logger.debug("Connection Setup Request forwarded to the next hop")
    return JSONResponse(
        content={"message": "Received connection setup request"},
        headers={"Content-Type": "application/json"},
    )


@router.post("/connection_setup_response")
@inject
async def handle_connection_setup_response(
    response: ConnectionSetupResponse,
    connection_manager: ConnectionManager = Depends(
        Provide[Container.connection_manager]
    ),
    routing_daemon: RoutingDaemon = Depends(Provide[Container.routing_daemon]),
    rule_engine: RuleEngine = Depends(Provide[Container.rule_engine]),
) -> dict:
    """
    Experimental function to handle connection setup responses
    :param response: ConnectionSetupResponse
    :return: dict
    """
    logger.debug("Received connection setup response")

    # Get proposed lau from rule engine based on current running ruleset
    proposed_la = rule_engine.accept_ruleset(response.connection_id, response.ruleset)

    # Get all the nighbor nodes to send laus
    neighbors = routing_daemon.get_neighbor_nodes()
    # Send LAU update to the next hop
    _ = await connection_manager.send_link_allocation_update(neighbors, proposed_la)

    # Get target pptsn with buffer from rule engine
    target_pptsns = rule_engine.get_pptsns_with_buffer(neighbors, 10)

    # Send barrier message
    await connection_manager.send_barrier(
        response.connection_id, neighbors, target_pptsns
    )

    # Update pending connection to running connection
    connection_manager.update_pending_connection_to_running_connection(
        response.connection_id, response.application_id
    )
    return JSONResponse(
        content={"message": "Received connection setup response"},
        headers={"Content-Type": "application/json"},
    )


@router.post("/connection_setup_reject")
@inject
async def handle_connection_setup_reject(reject: ConnectionSetupReject):
    return {"message": "Received connection setup reject"}


@router.post("/link_allocation_update")
@inject
async def handle_lau_update(
    proposed_lau: LinkAllocationUpdate,
    rule_engine: RuleEngine = Depends(Provide[Container.rule_engine]),
):
    """
    Receive link allocation from neighbor node which has larger ip address
    """
    logger.debug("Received LAU update")
    # Decide this lau is acceptable or not.
    # For now, the proposed lau is always acceptable at the first round
    (accepted, _new_proposed_lau) = rule_engine.accept_lau(proposed_lau)
    if accepted:
        # Send accept response
        return {"message": "LAU Accepted"}
    else:
        raise NotImplementedError("Unacceptable LAU is not yet implemented")


@router.post("/barrier")
@inject
async def handle_barrier(
    barrier: Barrier,
    connection_manager: ConnectionManager = Depends(
        Provide[Container.connection_manager]
    ),
    rule_engine: RuleEngine = Depends(Provide[Container.rule_engine]),
):
    """
    A neighbor with larger ip will send barrier message
    and this node (smaller ip) will respond to it
    """
    logger.debug(f"Received barrier from {barrier.header.src}")

    # Check this node's target pptsn and send back
    # This node's pptsn should always be larger since this node
    # is responding to the barrier message?
    pptsn_proposal = rule_engine.get_pptsns_with_buffer([barrier.header.src], 10)

    # compare with the received pptsn
    agreed_pptsn = max(pptsn_proposal[barrier.header.src], barrier.target_pptsn)

    response = await connection_manager.send_barrier_response(
        barrier.connection_id, barrier.header.src, agreed_pptsn
    )

    rule_engine.update_switching_pptsn(
        barrier.connection_id, barrier.header.src, agreed_pptsn
    )

    logger.debug(f"Barrier response sent: {response}")

    return {"message": "Received barrier"}


@router.post("/barrier_response")
@inject
async def handle_barrier_response(
    barrier: Barrier,
    rule_engine: RuleEngine = Depends(Provide[Container.rule_engine]),
):
    """
    At this moment, nodes must agree on one pptsn
    """
    logger.debug("Received barrier response")

    agreed_pptsn = barrier.target_pptsn

    # Update switching pptsn
    rule_engine.update_switching_pptsn(
        barrier.connection_id, barrier.header.src, agreed_pptsn
    )

    return {"message": "Received barrier response"}
