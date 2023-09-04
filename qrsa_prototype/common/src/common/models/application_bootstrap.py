from pydantic import BaseModel, Field

from common.type_utils import IpAddressType
from common.models import ApplicationPerformanceRequirement


class ApplicationBootstrap(BaseModel):
    destination: IpAddressType = Field(..., description="Destination IP address")
    application_performance_requirement: ApplicationPerformanceRequirement = Field(
        ..., description="Application performance requirement"
    )
