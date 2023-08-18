from enum import Enum
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import docker
from pydantic import BaseModel
from typing import Any, List, Dict, Annotated

api = FastAPI()
origins = [
     "http://127.0.0.1:5173",
     "http://localhost:5173"
     ]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContainerStatus(Enum):
    Running = "running"
    Stopped = "stopped"
    Restarting = "restarting"
    Paused = "paused"
    Exited = "exited"


class PortInfo(BaseModel):
    HostIp: str
    HostPort: str

class ProcessesInfo(BaseModel):
     Processes: List[List[str]]
     Titles: List[str]

class ContainerInfo(BaseModel):
    id: str
    name: str
    status: ContainerStatus
    attrs: Any
    ports: Dict[str, List[PortInfo]]
    top: ProcessesInfo

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

@api.post("/containers/{id}/start")
async def start_container(id, client:DockerClientDep):
     client.containers.get(id).start()

@api.post("/containers/{id}/stop")
async def stop_container(id, client:DockerClientDep):
     client.containers.get(id).stop()


@api.get("/containers/{id}/logs")
async def log_container(id, client:DockerClientDep):
     return {"logs": client.containers.get(id).logs()}

@api.get("/containers/{id}/diff")
async def diff_container(id, client:DockerClientDep):
     return {"diff": client.containers.get(id).diff()}

@api.post("/containers/{id}/exec_run" )
async def exec_run_container(id: str, cmd: str, client:DockerClientDep):
     return {"exec_result": client.containers.get(id).exec_run(cmd)}