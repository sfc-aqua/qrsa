from typing import NewType, Dict, Union
from pydantic import Field, BaseModel
from ipaddress import IPv4Address, IPv6Address

from common.models.application_performance_request import ApplicationPerformanceRequest
from common.models.header import Header
from common.models.performance_indicator import PerformanceIndicator

ApplicationId = NewType("ApplicationId", str)


class ConnectionSetupRequest(BaseModel):
    header: Header = Field(..., description="Header of the message")
    application_id: ApplicationId = Field(
        ..., description="Application Id which while connection id is not ready"
    )
    application_performance_request: ApplicationPerformanceRequest = Field(
        ..., description="The performance requirements for this application."
    )
    performance_indicators: Dict[
        Union[IPv4Address, IPv6Address], PerformanceIndicator
    ] = Field(..., description="The performance indicators for ruleset construction.")
