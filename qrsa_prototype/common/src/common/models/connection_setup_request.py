from pydantic import BaseModel, Field, NewType
from application_performance_request import ApplicationPerformanceRequest

ApplicationId = NewType("ApplicationId", str)


class ConnectionSetupRequest(BaseModel):
    application_id: ApplicationId = Field(
        ..., alias="Application Id which while connection id is not ready"
    )
    application_performance_request: ApplicationPerformanceRequest = Field(
        ..., alias="The performance requirements for this application."
    )
