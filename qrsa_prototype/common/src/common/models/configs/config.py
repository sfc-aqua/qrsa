from typing import Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from common.models.configs import (
    RoutingDaemonConfig,
    RuleEngineConfig,
    HardwareMonitorConfig,
    ConnectionManagerConfig,
    RealTimeControllerConfig,
)


class MetaInfo(BaseModel):
    """
    A model for meta information
    """

    ip_address: str = Field(..., description="IP address of the node")
    hostname: str = Field(..., description="Hostname of the node")


class Config(BaseSettings):
    """
    A model for input config
    """

    meta: MetaInfo = Field(..., description="Meta information of the node")
    routing_daemon: Optional[RoutingDaemonConfig] = Field(
        None, description="Routing daemon config"
    )
    rule_engine: Optional[RuleEngineConfig] = Field(
        None, description="Rule engine config"
    )
    hardware_monitor: Optional[HardwareMonitorConfig] = Field(
        None, description="Hardware monitor config"
    )
    connection_manager: Optional[ConnectionManagerConfig] = Field(
        None, description="Connection manager config"
    )
    real_time_controller: Optional[RealTimeControllerConfig] = Field(
        None, description="Real time controller config"
    )
