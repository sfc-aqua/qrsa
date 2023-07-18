use common::application_format::ApplicationRequestFormat;
use crate::connection::Connection;
use std::collections::HashMap;
use std::sync::{Arc, Mutex};

type ConnectionId = u128;
type ApplicationId = u128;
/// A main struct for Connection manager
///
pub struct ConnectionManager {
    /// A map of active running connections with connection id as a key
    /// This map is shared over multiple threads and multiple functions
    pub active_connections: Arc<Mutex<HashMap<ConnectionId, Connection>>>,
    /// A set of ids that are being set up
    pub pending_connections: Vec<ApplicationId>,
}

impl ConnectionManager {
    pub fn new() -> Self{
        ConnectionManager {
            active_connections: Arc::new(Mutex::new(HashMap::new())),
            pending_connections: vec![]
        }
    }

    /// Start running connection manager
    pub async fn boot(&self) {}

    /// An interface to the application
    /// The application manipulate this function to start the application
    /// When only the node type is initiator, this function can be executed
    ///
    ///
    #[cfg(feature = "initiator")]
    pub fn accept_application(&self, app_req: ApplicationRequestFormat) {
        
    }

    #[cfg(any(feature = "initiator", feature = "repeater"))]
    fn forward_connection_setup_request(&self){}

    /// Listen to incoming connection setup request
    /// This function wait for request from initiator
    ///
    #[cfg(any(feature = "repeater", feature = "responder"))]
    pub async fn listen_to_connection_setup_request(&self) {}

    /// Listen to incoming connection setup response
    ///
    #[cfg(any(feature = "initiator", feature = "repeater"))]
    pub async fn listen_to_connection_setup_response(&self) {}

    /// Listen to incoming connection setup reject
    ///
    #[cfg(any(feature = "initiator", feature = "repeater"))]
    pub async fn listen_to_connection_setup_reject(&self) {}

    #[cfg(feature = "repeater")]
    pub async fn listen_to_ruleset_termination(&self){}

    /// Listen to incoming LAU
    pub async fn listen_to_link_allocation_update() {}

    /// Listen to incoming Barrier
    ///
    pub async fn listen_to_barrier() {}
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_accept_application_request(){

    }

    #[tokio::test]
    async fn test_accept_connection_setup_request(){
        let connection_manager = ConnectionManager::new();
        // connection_manager.listen_to_connection_setup_request();
    }
}
