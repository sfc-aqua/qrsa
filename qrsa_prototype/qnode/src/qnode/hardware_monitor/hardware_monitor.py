from common.models.performance_indicator import PerformanceIndicator
from qnode.real_time_controller.real_time_controller import RealtimeController


class HardwareMonitor:
    def __init__(self, config: dict, rtc: RealtimeController):
        self.config = config
        # A realtime controller to control hardware devices
        self.rtc = rtc

    def get_performance_indicator(self) -> PerformanceIndicator:
        dummy_pi = PerformanceIndicator(local_op_fidelity=0.99)
        return dummy_pi
