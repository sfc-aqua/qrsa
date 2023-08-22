from dependency_injector import containers, providers

from qnode.connection_manager.connection_manager import ConnectionManager
from qnode.hardware_monitor.hardware_monitor import HardwareMonitor
from qnode.routing_daemon.routing_daemon import RoutingDaemon
from qnode.rule_engine.rule_engine import RuleEngine


class Container(containers.DeclarativeContainer):
    """
    A container class for dependency injections

    This is not thread safe. If the thread safety is needed, use ThreadSafeSingleton.
    """

    wiring_config = containers.WiringConfiguration(
        modules=["qnode.endpoints", "qnode.client"],
        packages=[
            "qnode.connection_manager",
            "qnode.hardware_monitor",
            "qnode.routing_daemon",
            "qnode.rule_engine",
        ],
    )
    config = providers.Configuration("config")

    connection_manager = providers.Singleton(
        ConnectionManager,
        config,
    )
    hardware_monitor = providers.Singleton(HardwareMonitor)
    routing_daemon = providers.Singleton(RoutingDaemon)
    rule_engine = providers.Singleton(RuleEngine, config)
