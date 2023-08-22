from abc import ABCMeta


class AbstractRealtimeController(metaclass=ABCMeta):
    def start_link_entanglement_generation(self):
        """
        Start link entanglement generation
        """
        pass

    def stop_link_entanglement_generation(self):
        """
        Stop link entanglement generation
        """
        pass

    async def fetch_link_entanglement(self):
        """
        Schedule link entanglement generation
        """
        pass
