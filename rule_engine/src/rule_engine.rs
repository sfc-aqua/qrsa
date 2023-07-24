use crate::la_policy_manager::LinkAllocationPolicyManager;
use crate::resource_allocator::ResourceAllocator;
use crate::scheduler::RuleSetScheduler;

/// A component that executes RuleSet
pub struct RuleEngine {
    resource_allocator: Box<ResourceAllocator>,
    /// One link allocation policy manager is created
    link_allocation_policy_managers: Vec<LinkAllocationPolicyManager>,
    ruleset_scheduler: Box<RuleSetScheduler>,
}

impl RuleEngine {
    pub fn new() {}

    pub async fn boot() {}

    /// Create a new policy manager that
    pub fn instantiate_policy_manager() {}

    /// Listen to new RuleSet coming from CM
    pub async fn wait_for_new_ruleset() {}
}

mod tests {}
