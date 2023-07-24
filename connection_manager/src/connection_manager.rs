use crate::{config::CmConfig, connection::Connection, error::ConnectionManagerError, IResult};

use config::Config;
use std::collections::HashMap;
use std::env;
use std::sync::{Arc, Mutex};
use tokio::{net::TcpListener, task};
use uuid::Uuid;

use common::application_format::ApplicationRequestFormat;

type ConnectionId = Uuid;

/// ApplicationId is used to identify which application is corresponding to which RuleSet
/// Initiator pass this id to responder and responder creates RuleSets and return them with this value
type ApplicationId = Uuid;
/// A main struct for Connection manager
///
pub struct ConnectionManager {
    /// A map of active running connections with connection id as a key
    /// This map is shared over multiple threads and multiple functions
    pub active_connections: Arc<Mutex<HashMap<ConnectionId, Connection>>>,
    /// A set of ids that are being set up
    pub pending_connections: Vec<ApplicationId>,
    // request from application
    #[cfg(feature = "initiator")]
    application_requirements: Vec<ApplicationRequestFormat>,
    // Config for connection mamanger
    config: CmConfig,
}

impl ConnectionManager {
    /// Create connection manager
    ///
    pub fn new() -> Self {
        let config_file_path = "Settings.toml";
        let config = Config::builder()
            .add_source(config::File::with_name(&config_file_path))
            .build()
            .unwrap()
            .try_deserialize()
            .unwrap();
        ConnectionManager {
            active_connections: Arc::new(Mutex::new(HashMap::new())),
            pending_connections: vec![],
            #[cfg(feature = "initiator")]
            application_requirement: vec![],
            config,
        }
    }

    /// Start running connection manager
    #[cfg(feature = "initiator")]
    pub async fn boot(&self) {
        let accept_app = task::spawn(self.accept_application);
        accept_app.await.unwrap();
        self.boot_listener().await.unwrap();
    }

    #[cfg(not(feature = "initiator"))]
    pub async fn boot(&self) {}

    async fn boot_listener(&self) -> IResult<()> {
        // Request neighbor information
        let socker_addr = format!("{}:{}", self.config.host, self.config.port);
        let listener = TcpListener::bind(addr).await.unwrap();
        Ok(())
    }

    /// An interface to the application
    /// The application manipulate this function to start the application
    /// When only the node type is initiator, this function can be executed
    ///
    #[cfg(feature = "initiator")]
    pub async fn accept_application(&mut self, app_req: ApplicationRequestFormat) {
        self.application_requirements.push(app_req);
    }

    #[cfg(any(feature = "initiator", feature = "repeater"))]
    async fn forward_connection_setup_request(&self) {}

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
    pub async fn listen_to_ruleset_termination(&self) {}

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
    fn test_read_config_file() {
        let cm = ConnectionManager::new();
        cm.boot();
    }

    #[test]
    fn test_accept_application_request() {}

    #[tokio::test]
    async fn test_accept_connection_setup_request() {
        let connection_manager = ConnectionManager::new();
        // connection_manager.listen_to_connection_setup_request();
    }
}
