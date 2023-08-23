import queue
from queue import Queue
from qnode.real_time_controller.interface import AbstractRealtimeController
from common.models.resource import ResourceMeta


class RealtimeController(AbstractRealtimeController):
    """
    A class to control hardware devices.

    This is used only from RuleEngine and HardwareMonitor.
    """

    def __init__(self):
        self.generating = False
        self.generated_link_entanglement: Queue[ResourceMeta] = Queue(maxsize=0)

    def start_link_entanglement_generation(self):
        if self.generating:
            raise RuntimeError("Link entanglement generation has already started")

        # Dummy resource meta
        self.generated_link_entanglement.put()
        self.generating = True

    def stop_link_entanglement_generation(self):
        if not self.generating:
            raise RuntimeError("Link entanglement generation is not started")

        self.generating = False

    async def fetch_link_entanglement(self):
        """
        Asyncronous generator that takes a resource from queue
        """
        try:
            yield self.generated_link_entanglement.get(block=True)
        except queue.Empty:
            # If there is no available link entanglement, return None
            yield None
