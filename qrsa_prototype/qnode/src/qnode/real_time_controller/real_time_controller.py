import queue
from queue import Queue
from typing import Dict

from qnode.real_time_controller.interface import AbstractRealtimeController
from common.models.resource import ResourceMeta
from common.type_utils import IpAddressType


class RealtimeController(AbstractRealtimeController):
    """
    A class to control hardware devices.

    This is used only from RuleEngine and HardwareMonitor.
    """

    def __init__(self, config: dict):
        self.config = config
        # neighbor address -> bool
        # A flag to indicate whether link entanglement generation is started
        self.generating: Dict[IpAddressType, bool] = {}
        self.generated_link_entanglement: Dict[IpAddressType, Queue[ResourceMeta]] = {}
        # neighbor address -> pptsn (int)
        # Track the current photon pair trial sequence number
        # of the link entanglement with neighbor node
        self.pptsn_record = {}

    def start_link_entanglement_generation(self, neighbor: IpAddressType):
        # If there is no neighbor record, this should be the first time
        if self.generating.get(neighbor, False):
            raise RuntimeError("Link entanglement generation has already started")

        self.generating[neighbor] = True
        # Create a queue to store generated link entanglement
        self.generated_link_entanglement[neighbor] = Queue(maxsize=0)

    def stop_link_entanglement_generation(self, neighbor: IpAddressType):
        # If there is no neighbor record, something wrong is happening
        if self.generating.get(neighbor) is None or not self.generating.get(neighbor):
            raise RuntimeError("Link entanglement generation is not started")

        self.generating[neighbor] = False
        # flush queue and initialize qubits
        self.generating[neighbor] = Queue(maxsize=0)

    async def fetch_link_entanglement(self, neighbor: IpAddressType):
        """
        Asyncronous generator that takes a resource from queue
        """
        try:
            yield self.generated_link_entanglement[neighbor].get(block=True)
        except queue.Empty:
            # If there is no available link entanglement, return None
            yield None

    def get_pptsn(self, neighbor: IpAddressType):
        """
        Get current pptsn and increment it by buffer
        """
        if self.pptsn_record.get(neighbor) is None:
            self.pptsn_record[neighbor] = 0
            return 0
        return self.pptsn_record[neighbor]
