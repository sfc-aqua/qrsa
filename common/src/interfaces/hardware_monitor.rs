use mockall::automock;

#[automock]
pub trait IHardwareMonitor {
    fn fetch_performance_indicator(&self);
}
