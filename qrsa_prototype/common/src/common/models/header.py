from typing import Union, Any
from pydantic import BaseModel, Field
from ipaddress import IPv4Address, IPv6Address


class Header(BaseModel):
    src: Union[IPv4Address, IPv6Address, str] = Field(
        ..., alias="Source ip addr of the message"
    )
    dst: Union[IPv4Address, IPv6Address, str] = Field(
        ..., alias="Destination ip addr of the message"
    )

    def __init__(self):
        super().__init__()
        # self.dst = dst
        # self.src = src

    def __new__(cls) -> Any:
        return super().__new__(cls)
