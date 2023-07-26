use crate::models::link_allocation_policy::LinkAllocationPolicy;
use mockall::automock;

#[automock]
pub trait IRuleEngine {
    fn accept_ruleset(&mut self) -> LinkAllocationPolicy;
}
