from typing import Union
from pydantic import BaseModel, Field
from ipaddress import IPv4Address, IPv6Address


class Header(BaseModel):
    src: Union[IPv4Address, IPv6Address, str] = Field(
        ..., description="Source ip addr of the message"
    )
    dst: Union[IPv4Address, IPv6Address, str] = Field(
        ..., description="Destination ip addr of the message"
    )
