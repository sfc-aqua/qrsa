from pydantic import BaseModel, Field


class ConnectionSetupReject(BaseModel):
    connection_id: str = Field(..., alias="Identifier for this connection")
    reason: str = Field(
        ..., alias="Reason for rejecting the connection request."
    )