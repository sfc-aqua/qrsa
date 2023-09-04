from dependency_injector import containers, providers

from qnode.real_time_controller import RealtimeController
from qnode.connection_manager import ConnectionManager
from qnode.hardware_monitor import HardwareMonitor
from qnode.routing_daemon import RoutingDaemon
from qnode.rule_engine import RuleEngine


class Container(containers.DeclarativeContainer):
    """
    A container class for dependency injections

    This is not thread safe. If the thread safety is needed, use ThreadSafeSingleton.
    """

    wiring_config = containers.WiringConfiguration(
        modules=["qnode.endpoints"],
        packages=["qnode"],
    )
    config = providers.Configuration("config")

    real_time_controller = providers.Singleton(RealtimeController, config)
    connection_manager = providers.Singleton(
        ConnectionManager,
        config,
    )
    hardware_monitor = providers.Singleton(
        HardwareMonitor, config, real_time_controller
    )
    routing_daemon = providers.Singleton(RoutingDaemon, config)
    rule_engine = providers.Singleton(RuleEngine, config, real_time_controller)
