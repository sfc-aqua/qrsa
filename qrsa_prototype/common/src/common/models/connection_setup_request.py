from pydantic import BaseModel, Field
from application_performance_request import ApplicationPerformanceRequest


class ConnectionSetupRequest(BaseModel):
    application_id: str = Field(
        ..., alias="Application Id which while connection id is not ready"
    )
    application_performance_request: ApplicationPerformanceRequest = Field(
        ..., alias="The performance requirements for this application."
    )
