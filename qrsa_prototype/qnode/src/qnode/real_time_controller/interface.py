from abc import ABCMeta, abstractmethod


class AbstractRealtimeController(metaclass=ABCMeta):
    @abstractmethod
    def start_link_entanglement_generation(self):
        """
        Start link entanglement generation
        """
        pass

    @abstractmethod
    def stop_link_entanglement_generation(self):
        """
        Stop link entanglement generation
        """
        pass

    @abstractmethod
    async def fetch_link_entanglement(self):
        """
        Schedule link entanglement generation
        """
        pass
