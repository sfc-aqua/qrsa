from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, Field
from controller.container import ContainerInfo

if TYPE_CHECKING:
    from common.type_utils import IpAddressType


class QNode:
    ip_address_list: "List[IpAddressType]"
    container: "ContainerInfo"
    id: str
    name: str

    def __init__(self, container: "Optional[ContainerInfo]" = None) -> None:
        if container is not None:
            self.container = container
            self.id = container.id
        else:
            raise RuntimeError("Not implemented yet")
        self.name = ""

    def dump_json(self):
        return QNodeData(
            ip_address_list=[],
            id=self.id,
            container=self.container,
            name=self.id if self.container is None else self.container.name,
        )


class QNodeData(BaseModel):
    ip_address_list: "List[str]"
    container: "Optional[ContainerInfo]"
    id: str
    name: str
