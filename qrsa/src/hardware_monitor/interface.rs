use crate::common::performance_indicator::PerformanceIndicator;
use mockall::automock;

#[automock]
pub trait IHardwareMonitor {
    fn get_performance_indicator(&self) -> PerformanceIndicator;
}
