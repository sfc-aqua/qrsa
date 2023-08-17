from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    message: str = Field(
        ..., description="Message to be returned to the client"
    )
