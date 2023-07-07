
/// A temporary structure that holds runtime execution ownership
pub struct LinkAllocationPolicyManager{

}

impl LinkAllocationPolicyManager{
    pub fn new(){

    }

    /// When the policy manager is initiated, it requests ownership to the running runtimes
    /// After Link Allocation Policy Manager got assigned a new available resource,
    /// it actually starts running runtime
    /// Until the previous policy is expired, it does not have permissions to execute
    pub fn claim_runtime_ownership(){

    }


}