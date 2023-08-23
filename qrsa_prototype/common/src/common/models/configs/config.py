from typing import List, Optional
from pydantic import BaseModel, Field

from common.models.configs.routing_daemon_config import RoutingDaemonConfig
from common.models.configs.rule_engine_config import RuleEngineConfig
from common.models.configs.hardware_monitor_config import HardwareMonitorConfig
from common.models.configs.connection_manager_config import ConnectionManagerConfig
from common.models.configs.real_time_controller_config import RealTimeControllerConfig


class MetaInfo(BaseModel):
    """
    A model for meta information
    """

    ip_address: str = Field(..., description="IP address of the node")
    hostname: str = Field(..., description="Hostname of the node")


class Config(BaseModel):
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
