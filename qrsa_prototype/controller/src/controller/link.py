from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from controller.qnode import QNode


class Link:
    id: str
    qnode1: "QNode"
    qnode2: "QNode"
    cost: float
    # ping info
    # cost
    # support node info
    # ip addr

    def __init__(self, qnode1: "QNode", qnode2: "QNode") -> None:
        self.qnode1 = qnode1
        self.qnode2 = qnode2
        self.id = (
            f"{qnode1.id}-{qnode2.id}"
            if qnode1.id > qnode2.id
            else f"{qnode2.id}-{qnode1.id}"
        )

    def dump_json(self) -> "LinkData":
        return LinkData(id=self.id, qnode1_id=self.qnode1.id, qnode2_id=self.qnode2.id)


class LinkData(BaseModel):
    id: str
    qnode1_id: str
    qnode2_id: str
