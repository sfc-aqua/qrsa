from typing import Optional, Tuple, Dict, List
from queue import Queue

from common.models import (
    RuleSet,
    ResourceMeta,
    LinkAllocationUpdate,
    LinkAllocationPolicy,
)
from common.type_utils import IpAddressType
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
        # neighbor address -> pptsn (int)
        # Track current sequence number of link entanglement with neighbor node
        self.current_pptsn = {}
        # A realtime controller to control hardware devices
        self.rtc = rtc
        # connection_id -> pptsn
        # Check when a new link allocation policy is activated
        self.la_switch_timings: Dict[str, Dict[IpAddressType, int]] = {}

    async def get_resource(self):
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

    def get_current_pptsn(
        self, neighbors: List[IpAddressType]
    ) -> Dict[IpAddressType, int]:
        return {neighbor: self.rtc.get_pptsn(neighbor) for neighbor in neighbors}

    def get_pptsns_with_buffer(
        self, neighbors: List[IpAddressType], buffer: int
    ) -> Dict[IpAddressType, int]:
        """
        Get current pptsn and increment it by buffer
        """
        return {
            neighbor: self.rtc.get_pptsn(neighbor) + buffer for neighbor in neighbors
        }

    def accept_ruleset(self, connection_id: str, ruleset: RuleSet):
        # TODO: implement policy and pptsn relationship

        if self.running_runtime.get(connection_id):
            # start link entanglement generation process
            self.rtc.start_link_entanglement_generation()

        # Initialize runtime
        runtime = RuleSetRuntime(ruleset)
        self.running_runtime[connection_id] = runtime

        # Once a new RuleSet is accepted, the link allocation plicy must be updated
        # Based on running rulesets, rule engine decides the next link allocation policy
        new_la = LinkAllocationUpdate(
            **{
                "connection_id": str(connection_id),
                "proposed_link_allocation": LinkAllocationPolicy(**{}),
            }
        )
        return new_la

    def accept_lau(
        self, lau: LinkAllocationUpdate
    ) -> Tuple[bool, Optional[LinkAllocationUpdate]]:
        """
        Check the currently running rulesets and
        decide whether to accept the LAU or not.
        """
        # If false, send new proposed LAU back
        # For now, rule engine always accepts lau
        return (True, None)

    def update_switching_pptsn(
        self, connection_id: str, neighbor: IpAddressType, target_pptsn: int
    ):
        # Need to check if the current pptsn is smaller than target pptsn
        if self.la_switch_timings.get(connection_id) is None:
            self.la_switch_timings[connection_id] = {}
        # Update switching pptsn
        self.la_switch_timings[connection_id][neighbor] = target_pptsn

    def get_switching_pptsns(
        self, connection_id: str, neighbors: List[IpAddressType]
    ) -> Dict[IpAddressType, int]:
        """
        Get switching pptsn based on the current running ruleset
        """
        return {
            neighbor: self.la_switch_timings[connection_id][neighbor]
            for neighbor in neighbors
        }

    def terminate_ruleset(self, connection_id: str):
        pass
