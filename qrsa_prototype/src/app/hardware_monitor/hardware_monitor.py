from common.model.performance_indicator import PerformanceIndicator


class HardwareMonitor:
    def __init__(self):
        pass

    def get_performance_indicator(self) -> PerformanceIndicator:
        dummy_pi = PerformanceIndicator(local_op_fidelity=0.99)
        return dummy_pi
