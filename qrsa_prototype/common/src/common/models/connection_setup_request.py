from typing import NewType, Any
from pydantic import Field
from common.models.application_performance_request import ApplicationPerformanceRequest
from common.models.header import Header

ApplicationId = NewType("ApplicationId", str)


class ConnectionSetupRequest(Header):
    application_id: ApplicationId = Field(
        ..., alias="Application Id which while connection id is not ready"
    )
    application_performance_request: ApplicationPerformanceRequest = Field(
        ..., alias="The performance requirements for this application."
    )

    def __init__(self, src, dst, application_id, application_performance_request):
        super().__init__(src, dst)
        self.application_id = application_id
        self.application_performance_request = application_performance_request

    def __new__(cls) -> Any:
        cls.__new__ = super().__new__
        return super().construct()
