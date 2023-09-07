
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


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
    top: Optional[ProcessesInfo]
