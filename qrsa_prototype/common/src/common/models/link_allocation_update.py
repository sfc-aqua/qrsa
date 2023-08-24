from pydantic import BaseModel, Field
from common.models.link_allocation_policy import LinkAllocationPolicy


class LinkAllocationUpdate(BaseModel):
    connection_id: str = Field(..., description="Identifier for this connection")
    proposed_link_allocations: LinkAllocationPolicy = Field(
        ..., description="A new link allocation policy"
    )
