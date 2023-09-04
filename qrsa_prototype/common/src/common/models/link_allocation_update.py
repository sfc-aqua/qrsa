from pydantic import BaseModel, Field
from common.models import LinkAllocationPolicy


class LinkAllocationUpdate(BaseModel):
    connection_id: str = Field(..., description="Identifier for this connection")
    proposed_link_allocation: LinkAllocationPolicy = Field(
        ..., description="A new link allocation policy"
    )
