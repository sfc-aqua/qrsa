from enum import Enum
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import docker
from pydantic import BaseModel
from typing import Any, List, Dict, Annotated

api = FastAPI()
origins = ["http://127.0.0.1:5173"]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/hello")
def read_root():
    return {"Hello": "World"}


class ContainerStatus(Enum):
    Running = "running"
    Stopped = "stopped"
    Restarting = "restarting"
    Paused = "paused"
    Exited = "exited"


class PortInfo(BaseModel):
    HostIp: str
    HostPort: str


class ContainerInfo(BaseModel):
    id: str
    name: str
    status: ContainerStatus
    attrs: Any
    ports: Dict[str, List[PortInfo]]

def DockerClient() -> docker.DockerClient:
        return docker.client.from_env()

DockerClientDep = Annotated[DockerClient, Depends()]

@api.get("/containers", response_model=List[ContainerInfo])
async def docker_ps(client:DockerClientDep):
    containers = [
        c for c in client.containers.list(all=True) if c.name.startswith("qrsa-")
    ]
    return [
        {
            "id": c.short_id,
            "name": c.name,
            "status": c.status,
            "top": c.top() if c.status == "running" else None,
            "attrs": c.attrs,
            "ports": c.ports,
        }
        for c in containers
    ]

@api.post("/containers/start/{id}")
async def start_container(id, client:DockerClientDep):
     client.containers.get(id).start()

@api.post("/containers/stop/{id}")
async def stop_container(id, client:DockerClientDep):
     client.containers.get(id).stop()

