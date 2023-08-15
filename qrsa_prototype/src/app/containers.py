from dependency_injector import containers, providers

from connection_manager.connection_manager import ConnectionManager
from hardware_monitor.hardware_monitor import HardwareMonitor
from routing_daemon.routing_daemon import RoutingDaemon
from rule_engine.rule_engine import RuleEngine


class Container(containers.DeclarativeContainer):
    """
    A container class for dependency injections

    This is not thread safe. If the thread safety is needed, use ThreadSafeSingleton.
    """

    config = providers.Configuration()

    connection_manager = providers.Singleton(ConnectionManager)

    hardware_monitor = providers.Singleton(HardwareMonitor)

    routing_daemon = providers.Singleton(RoutingDaemon)

    rule_engine = providers.Singleton(RuleEngine)
