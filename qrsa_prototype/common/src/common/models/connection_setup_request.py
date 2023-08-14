from typing import NewType
from pydantic import Field, BaseModel
from common.models.application_performance_request import ApplicationPerformanceRequest
from common.models.header import Header

ApplicationId = NewType("ApplicationId", str)


class ConnectionSetupRequest(BaseModel):
    header: Header = Field(..., description="Header of the message")
    application_id: ApplicationId = Field(
        ..., description="Application Id which while connection id is not ready"
    )
    application_performance_request: ApplicationPerformanceRequest = Field(
        ..., description="The performance requirements for this application."
    )
