from datetime import datetime, timedelta
from typing import Dict, List, Optional, Coroutine

import docker

from pydantic import BaseModel, Field
from controller.container import ContainerInfo
from common.type_utils import IpAddressType


class QNode:
    ip_address_list: "List[IpAddressType]"
    container: "ContainerInfo"
    id: str
    name: str
    ping: Dict[str, Dict[str, float]]
    log_retrieved_at: datetime

    def __init__(self, container: "Optional[ContainerInfo]" = None) -> None:
        if container is not None:
            self.container = container
            self.id = container.id
        else:
            raise RuntimeError("Not implemented yet")
        self.name = ""
        self.log_retrieved_at = datetime.now() - timedelta(hours=1)

    def dump_json(self):
        return QNodeData(
            ip_address_list=[],
            id=self.id,
            container=self.container,
            name=self.id if self.container is None else self.container.name,
        )

    def get_log(
        self, client: Optional[docker.DockerClient] = None
    ) -> Coroutine[bytes, None, None]:
        if self.container is None:
            raise RuntimeError("not implemented yet")
        if client is None:
            raise RuntimeError("docker container requires docker client")
        since = self.log_retrieved_at
        self.log_retrieved_at = datetime.now()
        print(since)
        return client.containers.get(self.id).logs(since=since)

    def ping(self, client: docker.DockerClient, target_host: IpAddressType):
        result = self.run_cmd_stream(f"ping {target_host}", client)
        for output, _ in result:
            s = [
                chunk for chunk in output.decode("utf-8").split(" ") if "time=" in chunk
            ]
            if not s:
                continue
            [_, t] = s[0].split("=")
            print(float(t))

    def run_cmd_stream(
        self, cmd: str, client: Optional[docker.DockerClient] = None
    ) -> Coroutine[bytes, None, None]:
        if self.container is None:
            raise RuntimeError("not implemented yet")
        if client is None:
            raise RuntimeError("docker container requires docker client")
        (_, result) = client.containers.get(self.container.id).exec_run(
            cmd, stream=True, stdout=True, stderr=True, tty=True, demux=True
        )
        return result


class QNodeData(BaseModel):
    ip_address_list: "List[str]"
    container: "Optional[ContainerInfo]"
    id: str
    name: str
