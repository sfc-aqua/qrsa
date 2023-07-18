use std::time::SystemTime;

/// An identifier for one generated link resource
/// Need
/// - resource type identifier
/// - timestamp
/// - current owner
/// - PPTSN (Photon Pair Trial Sequence Number)
pub struct ResourceId{
    /// sequencial number identifier of resource
    id: u128,
    /// The timestamp that this resource is created and ready
    created_at: SystemTime
}


pub enum ResourceType{
    Bell(BellState),
    Graph,
}


pub struct BellState{}