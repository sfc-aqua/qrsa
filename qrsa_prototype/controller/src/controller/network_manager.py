from typing import List, Optional

import docker
from pydantic import BaseModel

from controller.container import ContainerInfo
from controller.link import Link, LinkData
from controller.qnode import QNode, QNodeData


class NetworkData(BaseModel):
    qnodes: List[QNodeData]
    links: List[LinkData]


class NetworkManager:
    qnodes: "List[QNode]"
    links: "List[Link]"
    docker_client: "docker.DockerClient"

    def __init__(self) -> None:
        self.docker_client = docker.client.from_env()
        self.qnodes = []
        self.links = []

    def fetch_network_info(self):
        containers = [
            c
            for c in self.docker_client.containers.list(all=True)
            if c.name.startswith("qrsa-") and not c.name.startswith("qrsa-controller")
        ]
        container_info_list = [
            ContainerInfo(
                id=c.short_id,
                name=c.name,
                status=c.status,
                top=c.top() if c.status == "running" else None,
                attrs=c.attrs,
                ports=c.ports,
            )
            for c in containers
        ]

        current_qnode_ids = [q.id for q in self.qnodes]

        for c in container_info_list:
            if c.id not in current_qnode_ids:
                self.append_qnode_from_container(c)
            else:
                self.update_qnode_info(c)

        for q1 in self.qnodes:
            for q2 in self.qnodes:
                if q1.id == q2.id:
                    continue
                link = self.get_link_by_qnode_ids(q1.id, q2.id)
                if link is None:
                    self.links.append(Link(q1, q2))

    def get_qnode(self, id: str) -> Optional[QNode]:
        if not self.qnodes:
            return None
        return next(filter(lambda q: q.id == id, self.qnodes))

    def get_network(self) -> "NetworkData":
        return NetworkData(
            qnodes=[qnode.dump_json() for qnode in self.qnodes],
            links=[link.dump_json() for link in self.links],
        )

    def get_link_by_qnode_ids(self, qnode1_id: str, qnode2_id: str) -> Optional[Link]:
        if not self.links:
            return None
        id = (
            f"{qnode1_id}-{qnode2_id}"
            if qnode1_id > qnode2_id
            else f"{qnode2_id}-{qnode1_id}"
        )
        for l in self.links:
            if l.id == id:
                return l
        return None

    def append_qnode_from_container(self, container: "ContainerInfo"):
        """append qnode instance by docker container information."""
        self.qnodes.append(QNode(container))

    def update_qnode_info(self, container_info: "ContainerInfo"):
        """update qnode's container information. if the qnode doesn't exist, ignore it."""
        qnode: "Optional[QNode]" = next(
            filter(lambda q: q.id == container_info.id, self.qnodes)
        )
        if qnode is None:
            return
        qnode.container = container_info
