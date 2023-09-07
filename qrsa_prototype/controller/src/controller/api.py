from controller.container import ContainerInfo
from controller.link import LinkData
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import docker
from typing import List, Annotated, Optional
from controller.pumba import PumbaDelayDistribution
from controller import network_manager

api = FastAPI()
origins = ["http://127.0.0.1:5173", "http://localhost:5173"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def DockerClient() -> docker.DockerClient:
    return docker.client.from_env()


__network_manager = network_manager.NetworkManager()


def NetworkManager() -> network_manager.NetworkManager:
    return __network_manager


DockerClientDep = Annotated[DockerClient, Depends()]
NetworkManagerDep = Annotated[NetworkManager, Depends()]


@api.get("/network", response_model=network_manager.NetworkData)
async def get_network(nm: NetworkManagerDep):
    nm.fetch_network_info()
    return nm.get_network()


@api.post("/containers/{id}/start")
async def start_container(id, client: DockerClientDep):
    client.containers.get(id).start()


@api.post("/containers/{id}/stop")
async def stop_container(id, client: DockerClientDep):
    client.containers.get(id).stop()


@api.get("/containers/{id}/logs")
async def log_container(id, client: DockerClientDep):
    return {"logs": client.containers.get(id).logs()}


@api.get("/containers/{id}/diff")
async def diff_container(id, client: DockerClientDep):
    return {"diff": client.containers.get(id).diff()}


@api.post("/containers/{id}/exec_run")
async def exec_run_container(id: str, cmd: str, client: DockerClientDep):
    (exit_code, result) = client.containers.get(id).exec_run(cmd, stream=False)
    return {"exec_result": result, "exit_code": exit_code}


@api.post("/containers/{id}/exec_run_stream", response_class=StreamingResponse)
async def exec_run_container_stream(id: str, cmd: str, client: DockerClientDep):
    (_, result) = client.containers.get(id).exec_run(
        cmd, stream=True, stdout=True, stderr=True
    )
    return StreamingResponse(content=result, media_type="text/plain")


@api.post("/links/{id}/delay")
async def set_delay(
    id,
    time: float,
    jitter: float,
    correlation: float,
    distribution: Optional[PumbaDelayDistribution],
):
    pass
