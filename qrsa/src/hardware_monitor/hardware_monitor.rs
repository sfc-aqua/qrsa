use crate::common::performance_indicator::PerformanceIndicator;

use super::interface::IHardwareMonitor;

/// Hardware monitor structure
///
///
pub struct HardwareMonitor {}

/// Hardware Monitor implementation
///
impl HardwareMonitor {
    pub fn new() {}

    /// Start Link Generation process
    pub async fn start_photon_link_generation() {
        // link generation process is different for device types
        // e.g. EPPS, BSA, RGS, ...
    }

    /// Notify link resource is ready to Rule Engine
    pub async fn notify_link_resource_ready() {}

    /// Perform link tomography between neighbor node
    ///
    ///
    pub async fn start_link_tomography() {
        // 1. Send link tomography
        // 2. Receive link tomography response (Decide which is primary node)
        // 3. Create link toography strategy (If primary)
        // 4. Send link tomography strategy (If primary)
        // 5. Link tomography strategy response
        // 6. Start link tomography
    }

    /// Fetch network peripheral devices that does not appear in the routing table
    /// such as EPPS, BSA
    pub async fn fetch_peripheral_info() {}

    /// Calculate link cost based on link tomography results
    fn calculate_link_cost() {}
}

impl IHardwareMonitor for HardwareMonitor {
    fn get_performance_indicator(&self) -> PerformanceIndicator {
        PerformanceIndicator::default()
    }
}
