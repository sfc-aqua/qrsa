from pydantic import BaseModel, Field

from common.models.header import Header


class Barrier(BaseModel):
    header: Header = Field(..., description="Header of the message.")
    connection_id: str = Field(..., description="Connection ID.")
    target_pptsn: int = Field(
        ..., ge=0, description="Target photon pair trial sequence number."
    )
