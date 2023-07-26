use async_trait::async_trait;
use config::Config;
use std::collections::HashMap;
use std::marker::Send;
use std::sync::{Arc, Mutex};
use tokio::net::TcpListener;
use uuid::Uuid;

use super::IResult;
use crate::connection_manager::config::config::CmConfig;
use crate::connection_manager::connection::connection::Connection;
use crate::connection_manager::error::ConnectionManagerError;
use crate::connection_manager::interface::IConnectionManager;

use crate::common::application_request_format::ApplicationRequestFormat;
use crate::common::performance_indicator::PerformanceIndicator;
use crate::hardware_monitor::interface::IHardwareMonitor;
use crate::rule_engine::interface::IRuleEngine;

type ConnectionId = Uuid;

/// ApplicationId is used to identify which application is corresponding to which RuleSet
/// Initiator pass this id to responder and responder creates RuleSets and return them with this value
type ApplicationId = Uuid;

/// A main struct for Connection Manager that stores running connection information and
/// manages them
pub struct ConnectionManager<HM, RE>
where
    HM: IHardwareMonitor + Send,
    RE: IRuleEngine + Send,
{
    /// A map of active running connections with connection id as a key
    /// This map is shared over multiple threads and multiple functions
    pub active_connections: Arc<Mutex<HashMap<ConnectionId, Connection>>>,
    /// A set of ids that are being set up
    pub pending_connections: Arc<Mutex<Vec<ApplicationId>>>,
    // Reference to hardware monitor. hardware monitor should live until it's terminated.
    hardware_monitor: Arc<Mutex<HM>>,
    // Reference to rule engine
    rule_engine: Arc<Mutex<RE>>,
    // Latest performance indicator to pass the hardware information
    performance_indicator: Option<PerformanceIndicator>,
    // request from application
    #[cfg(feature = "initiator")]
    application_requirements: Arc<Mutex<Vec<ApplicationRequestFormat>>>,
    // Config for connection mamanger
    config: CmConfig,
}

#[async_trait]
impl<HM, RE> IConnectionManager for ConnectionManager<HM, RE>
where
    HM: IHardwareMonitor + Send,
    RE: IRuleEngine + Send,
{
    #[cfg(feature = "initiator")]
    async fn accept_application(&mut self, app_req: ApplicationRequestFormat) {
        println!("{:#?}", app_req);
        self.application_requirements.lock().unwrap().push(app_req);
    }
}

impl<HM, RE> ConnectionManager<HM, RE>
where
    HM: IHardwareMonitor + Send,
    RE: IRuleEngine + Send,
{
    /// Create connection manager
    ///
    pub fn new(hardware_monitor: Arc<Mutex<HM>>, rule_engine: Arc<Mutex<RE>>) -> Self {
        let config_file_path = "Settings.toml";
        let config = Config::builder()
            .add_source(config::File::with_name(&config_file_path))
            .build()
            .unwrap()
            .try_deserialize()
            .unwrap();
        ConnectionManager {
            active_connections: Arc::new(Mutex::new(HashMap::new())),
            pending_connections: Arc::new(Mutex::new(vec![])),
            hardware_monitor,
            rule_engine,
            performance_indicator: None,
            #[cfg(feature = "initiator")]
            application_requirements: Arc::new(Mutex::new(vec![])),
            config,
        }
    }

    // /// Start running connection manager
    // #[cfg(feature = "initiator")]
    // async fn boot(&mut self) {
    //     // Get performance indicator
    //     self.request_performance_indicator()
    // }

    // #[cfg(not(feature = "initiator"))]
    // async fn boot(&mut self) {
    // }

    async fn boot_listener(&self) {
        // TODO: Request neighbor information to RD here
        let socket_addr = format!("{}:{}", self.config.host, self.config.port);
        let listener = TcpListener::bind(socket_addr).await.unwrap();
        // loop {
        //     let (socket, _) = listener.accept().await.unwrap();
        //     tokio::spawn(async {
        //         self.handle_connection(socket)
        //     });
        // }
    }

    fn request_performance_indicator(&mut self) {
        // Request performance indicator to hardware monitor
        if cfg!(test) {
            self.performance_indicator = Some(PerformanceIndicator::default())
        } else {
            // Fetch current performance indicator from HM
        }
    }

    async fn handle_connection(&self, socket: tokio::net::TcpStream) {}
    /// An interface to the application
    /// The application manipulate this function to start the application
    /// When only the node type is initiator, this function can be executed
    ///
    #[cfg(feature = "initiator")]
    pub async fn accept_application(&mut self, app_req: ApplicationRequestFormat) {}

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
    use crate::hardware_monitor::interface::MockIHardwareMonitor;
    use crate::rule_engine::interface::MockIRuleEngine;

    // test for common function
    #[test]
    fn test_init() {
        let mock_hardware_monitor = Arc::new(Mutex::new(MockIHardwareMonitor::default()));
        let mock_rule_engine = Arc::new(Mutex::new(MockIRuleEngine::default()));
        let connection_manager = ConnectionManager::new(mock_hardware_monitor, mock_rule_engine);
    }

    #[test]
    fn test_read_config_file() {
        // let cm = ConnectionManager::new();
    }

    #[tokio::test]
    async fn test_accept_connection_setup_request() {
        // let connection_manager = ConnectionManager::new();
        // connection_manager.listen_to_connection_setup_request();
    }

    #[cfg(test)]
    #[cfg(feature = "initiator")]
    mod initiator_tests {
        use super::*;
        #[test]
        fn test_initiator() {
            assert_eq!(1, 1)
        }

        #[tokio::test]
        async fn test_accept_application_request() {
            let mock_hardware_monitor = Arc::new(Mutex::new(MockIHardwareMonitor::default()));
            let mock_rule_engine = Arc::new(Mutex::new(MockIRuleEngine::default()));

            let mut connection_manager =
                ConnectionManager::new(mock_hardware_monitor, mock_rule_engine);
            let application_request_format = ApplicationRequestFormat::default();
            connection_manager
                .accept_application(application_request_format)
                .await;
            assert_eq!(
                connection_manager
                    .application_requirements
                    .lock()
                    .unwrap()
                    .len(),
                1
            );
        }
    }
}
