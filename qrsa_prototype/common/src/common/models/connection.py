from typing import Union
from pydantic import BaseModel, Field
from ipaddress import IPv4Address, IPv6Address


class ConnectionMeta(BaseModel):
    """
    ConnectionMeta is a model for the metadata of a connection
    This meta data is used in ConnectionManager to identify the destinations
    """

    prev_hop: Union[IPv4Address, IPv6Address, str, None] = Field(
        ..., description="The previous hop of this connection in the path"
    )
    next_hop: Union[IPv4Address, IPv6Address, str, None] = Field(
        ..., description="The next hop of this connection in the path"
    )
    source: Union[IPv4Address, IPv6Address, str] = Field(
        ..., description="The source of this connection"
    )
    destination: Union[IPv4Address, IPv6Address, str] = Field(
        ..., description="The destination of this connection"
    )
