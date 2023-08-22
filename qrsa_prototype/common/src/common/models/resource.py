import time
from pydantic import BaseModel, Field


class ResourceMeta(BaseModel):
    """
    Resource model that identify a qubit
    """

    resource_id: str = Field(..., description="An identifier of this resource")
    pptsn: int = Field(..., description="Photon pair trial sequence number")
    created_at: float = Field(
        time.time(), description="Timestamp when this resource is created"
    )
