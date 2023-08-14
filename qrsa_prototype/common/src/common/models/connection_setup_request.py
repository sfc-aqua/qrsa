from typing import NewType
from pydantic import Field, BaseModel
from common.models.application_performance_request import ApplicationPerformanceRequest
from common.models.header import Header

ApplicationId = NewType("ApplicationId", str)


class ConnectionSetupRequest(BaseModel):
    header: Header = Field(..., alias="Header of the message")
    application_id: ApplicationId = Field(
        ..., alias="Application Id which while connection id is not ready"
    )
    application_performance_request: ApplicationPerformanceRequest = Field(
        ..., alias="The performance requirements for this application."
    )
