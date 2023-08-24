from typing import Union, Optional, Tuple, Dict
from queue import Queue

from common.models.ruleset import RuleSet
from common.models.resource import ResourceMeta
from common.models.link_allocation_update import LinkAllocationUpdate
from common.log.logger import logger

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

    async def get_resource(self, resource_meta: ResourceMeta):
        """
        Accept a resource from RTC.

        :param resource_meta: ResourceMeta
        """
        trial = 0
        while True:
            resource = await self.rtc.fetch_link_entanglement()
            if resource is not None:
                self.available_link_resource.put(resource)
                break
            trial += 1
            if trial > 10:
                logger.warning("Resource is not availbe after 10 attempts")
                break

    def get_available_link_resource(self) -> ResourceMeta:
        return self.available_link_resource.get()

    def accept_lau(
        self, lau: LinkAllocationUpdate
    ) -> Tuple[bool, Optional[LinkAllocationUpdate]]:
        """
        Check the currently running rulesets and decide whether to accept the LAU or not.
        """
        # If false, send new proposed LAU back
        # For now, rule engine always accepts lau
        return (True, None)

    def accept_ruleset(self, connection_id: str, ruleset: RuleSet):
        # TODO: implement policy and pptsn relationship

        if self.running_runtime.get(connection_id):
            # start link entanglement generation process
            self.rtc.start_link_entanglement_generation()

        # Initialize runtime
        runtime = RuleSetRuntime(ruleset)
        self.running_runtime[connection_id] = runtime

    def terminate_ruleset(self, connection_id: str):
        pass
