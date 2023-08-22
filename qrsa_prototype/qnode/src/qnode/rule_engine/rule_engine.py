from typing import Dict
from queue import Queue

from common.models.ruleset import RuleSet
from common.models.resource import ResourceMeta

from qnode.rule_engine.ruleset_runtime import RuleSetRuntime
from qnode.real_time_controller.real_time_controller import RealtimeController


class RuleEngine:
    def __init__(self, config: dict, rtc: RealtimeController):
        self.config = config
        # connection_id -> ruleset_runtime
        self.running_runtime: Dict[str, RuleSetRuntime] = {}
        # When RTC notify the link entanglement is ready, meta information
        # of the link will be put into this queue
        self.available_link_resource: Queue[ResourceMeta] = Queue(maxsize=0)
        # A realtime controller to control hardware devices
        self.rtc = rtc

    def accept_resource(self, resource_meta: ResourceMeta):
        """
        Accept a resource from RTC.

        :param resource_meta: ResourceMeta
        """
        self.available_link_resource.put(resource_meta)

    def get_available_link_resource(self) -> ResourceMeta:
        return self.available_link_resource.get()

    def accept_ruleset(self, connection_id: str, ruleset: RuleSet):
        # TODO: implement policy and pptsn relationship

        # Initialize runtime
        runtime = RuleSetRuntime(ruleset)
        self.running_runtime[connection_id] = runtime
