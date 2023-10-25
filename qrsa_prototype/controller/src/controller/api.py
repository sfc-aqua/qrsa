import asyncio
from datetime import datetime, timedelta, timezone
from controller.container import ContainerInfo
from controller.event_collector import (
    log_collector,
    network_collector,
    qnode_status_collector,
)
from controller.link import LinkData
from controller.utils import PubSub
from fastapi import Depends, FastAPI, Response, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import docker
from typing import Optional
from typing_extensions import TypedDict
from controller.pumba import PumbaDelayDistribution
from controller import network_manager


class LogResult(TypedDict):
    logs: str


api = FastAPI()
ws_sessions = set()
origins = ["http://127.0.0.1:5173", "http://localhost:5173"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

__network_manager = network_manager.NetworkManager()
channel = PubSub()


def Channel() -> PubSub:
    return channel


def NetworkManager() -> network_manager.NetworkManager:
    return __network_manager


def DockerClient() -> docker.DockerClient:
    return docker.client.from_env()


@api.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    loop.create_task(log_collector(__network_manager, channel))
    loop.create_task(network_collector(__network_manager, channel))
    loop.create_task(qnode_status_collector(__network_manager, channel))


@api.on_event("shutdown")
async def shutdown():
    pass


@api.websocket("/ws")
async def ws_endpoint(ws: WebSocket, channel: PubSub = Depends(Channel)):
    await ws.accept()
    ws_sessions.add(ws)
    event_queue: asyncio.Queue[str] = asyncio.Queue()

    def receive_event(data: str):
        nonlocal event_queue
        event_queue.put_nowait(data)

    channel.subscribe(receive_event)

    while True:
        try:
            log = await event_queue.get()
            await ws.send_text(log)
            event_queue.task_done()
        except WebSocketDisconnect:
            break
        except asyncio.CancelledError:
            break

    channel.unsubscribe(receive_event)


@api.get("/network", response_model=network_manager.NetworkData)
async def get_network(nm: network_manager.NetworkManager = Depends(NetworkManager)):
    nm.fetch_network_info()
    return nm.get_network()


@api.post("/containers/{id}/start")
async def start_container(id, client: docker.DockerClient = Depends(DockerClient)):
    client.containers.get(id).start()  # type: ignore


@api.post("/containers/{id}/stop")
async def stop_container(id, client: docker.DockerClient = Depends(DockerClient)):
    client.containers.get(id).stop()  # type: ignore


@api.get("/containers/{id}/logs")
async def log_container(
    id,
    client: docker.DockerClient = Depends(DockerClient),
    nm: network_manager.NetworkManager = Depends(NetworkManager),
) -> Optional[LogResult]:
    qnode = nm.get_qnode(id)
    if qnode is None:
        return None
    logs = qnode.get_log(client)
    return {"logs": logs}


@api.get("/containers/{id}/clear_log_retrieval_at")
def clear_log_retrieval_at(
    id, nm: network_manager.NetworkManager = Depends(NetworkManager)
):
    qnode = nm.get_qnode(id)
    if qnode is None:
        return None
    qnode.log_retrieved_at = datetime.now() - timedelta(hours=1)


@api.get("/containers/{id}/diff")
async def diff_container(id, client: docker.DockerClient = Depends(DockerClient)):
    return {"diff": client.containers.get(id).diff()}  # type: ignore


@api.post("/containers/{id}/exec_run")
async def exec_run_container(
    id: str, cmd: str, client: docker.DockerClient = Depends(DockerClient)
):
    (exit_code, result) = client.containers.get(id).exec_run(cmd, stream=False)  # type: ignore
    return {"exec_result": result, "exit_code": exit_code}


@api.post("/containers/{id}/exec_run_stream", response_class=StreamingResponse)
async def exec_run_container_stream(
    id: str, cmd: str, client: docker.DockerClient = Depends(DockerClient)
):
    (_, result) = client.containers.get(id).exec_run(  # type: ignore
        cmd, stream=True, stdout=True, stderr=True
    )
    return StreamingResponse(content=result, media_type="text/plain")


@api.post("/container/{id}/start_connection_setup")
async def startConnectionSetup(
    id: str,
    destination: str,
    minimum_fidelity: float,
    minimum_bell_pair_bandwidth: int,
    response: Response,
    nm: network_manager.NetworkManager = Depends(NetworkManager),
):
    qnode = nm.get_qnode(id)
    if qnode is None:
        response.status_code = 404
        return {"message": f"qnode {id} not found"}
    dest_qnode = nm.get_qnode(destination)
    if dest_qnode is None:
        response.status_code = 404
        return {"message": f"dest node {destination} not found"}

    resp, status = await qnode.start_connection_setup(
        dest_qnode.ip_address_list[0], minimum_fidelity, minimum_bell_pair_bandwidth
    )
    response.status_code = 201
    return {"message": resp, "status": status}


@api.post("/links/{id}/delay")
async def set_delay(
    id,
    time: float,
    jitter: float,
    correlation: float,
    distribution: Optional[PumbaDelayDistribution],
):
    pass
