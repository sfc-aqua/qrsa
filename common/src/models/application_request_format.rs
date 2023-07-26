use crate::models::resources::ResourceType;
use core::time::Duration;

/// A format for application to send requirements of generated entanglements
///
#[derive(Default, Debug)]
pub struct ApplicationRequestFormat {
    /// The number of e2e requred
    pub num_pairs: u64,
    /// Time constrains for preparation time
    pub timeout: Duration,
    /// Minimum fidelity of the generated resources
    pub threshold_fidelity: f64,
    /// If this value is true, fidelity is higher priority
    /// and time would exceed
    pub prioritize_fidelity: bool,
}

impl ApplicationRequestFormat {
    pub fn new(num_pairs: u64, resource_type: Option<ResourceType>) {}
    // match resource_type{
    //     Some(res_type) => {

    //     },
    //     None => {
    //         ApplicationRequestFormat {
    //             num_pairs,
    //             ResourceType::Bell,
    //         }
    //     }
    // }
}
