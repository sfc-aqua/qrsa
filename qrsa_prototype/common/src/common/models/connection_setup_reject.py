from pydantic import BaseModel, Field


class ConnectionSetupReject(BaseModel):
    connection_id: str = Field(..., description="Identifier for this connection")
    reason: str = Field(..., description="Reason for rejecting the connection request.")
