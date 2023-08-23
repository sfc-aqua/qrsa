from enum import List, Optional, Enum
from pydantic import BaseModel, Field, validator

from common.type_utils import IpAddressType


class RoutingType(str, Enum):
    """
    A routing type enum
    """

    STATIC = "static"
    DYNAMIC = "dynamic"


class RouteInfo(BaseModel):
    """
    A model for routing information
    """

    destination: IpAddressType = Field(..., description="Destination IP address")
    name: Optional[str] = Field(None, description="Name of the destination")
    next_hop: IpAddressType = Field(..., description="Next hop IP address")


class RoutingDaemonConfig(BaseModel):
    """
    A configuration model for routing model
    """

    routing_type: RoutingType = Field(
        ...,
        description="Routing type name. This coule be routing protocol in the future.",
    )
    routing_table: List[RouteInfo] = Field(..., description="Routing table")

    @validator("routing_table", pre=True, always=True)
    def validate_routing_table(cls, routing_table, values):
        routing_type = values.get("routing_type")
        if routing_type == RoutingType.STATIC and routing_table is None:
            raise ValueError("Routing table must be provided for static routing")
        return routing_table
