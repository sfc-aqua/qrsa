use crate::routing_daemon::interface::IRoutingDaemon;
use crate::{cfg_initiator, cfg_repeater, cfg_responder, routing_daemon};
use async_trait::async_trait;
use std::collections::HashMap;
use std::marker::Send;
use std::net::SocketAddr;
use std::sync::{Arc, Mutex};

use bytes::BytesMut;
use tokio::net::{TcpListener, TcpStream};
use tokio_serde::{Deserializer, Serializer};
use tokio_stream::StreamExt;
use tokio_util::codec::{FramedRead, LengthDelimitedCodec};

// use super::IResult;
use crate::connection_manager::config::model::CmConfig;
use crate::connection_manager::connection::connection::Connection;
use crate::connection_manager::connection::id::{ApplicationId, ConnectionId};
use crate::connection_manager::error::ConnectionManagerError;
use crate::connection_manager::interface::IConnectionManager;

use crate::common::application_request_format::ApplicationRequestFormat;
use crate::common::performance_indicator::PerformanceIndicator;
use crate::hardware_monitor::interface::IHardwareMonitor;
use crate::rule_engine::interface::IRuleEngine;

/// A main struct for Connection Manager that stores running connection information and
/// manages them
pub struct ConnectionManager<HM, RE, RD>
where
    HM: IHardwareMonitor + Send,
    RE: IRuleEngine + Send,
    RD: IRoutingDaemon + Send,
{
    /// A map of tcp sockets with ip address as a key
    /// This map is shared over multiple threads and multiple functions
    /// The corresponding TcpStream is used to send data to the other nodes
    /// Currently, IpAddr should be good enough to identify the node
    pub tcp_sockets: Arc<Mutex<HashMap<SocketAddr, TcpStream>>>,
    /// A map of active running connections with connection id as a key
    /// This map is shared over multiple threads and multiple functions
    pub active_connections: Arc<Mutex<HashMap<ConnectionId, Connection>>>,
    /// A set of ids that are being set up
    pub pending_connections: Arc<Mutex<Vec<ApplicationId>>>,
    // Latest performance indicator to pass the hardware information
    performance_indicator: Option<PerformanceIndicator>,
    // Config for connection mamanger
    config: CmConfig,
    // request from application
    application_requirements: Arc<Mutex<Vec<ApplicationRequestFormat>>>,

    // Reference to hardware monitor. hardware monitor should live until it's terminated.
    hardware_monitor: Arc<Mutex<HM>>,
    // Reference to rule engine
    rule_engine: Arc<Mutex<RE>>,
    // Reference to routing daemon
    routing_daemon: Arc<Mutex<RD>>,
    #[cfg(features = "initiator")]
    test:u32,
}

#[async_trait]
impl<HM, RE, RD> IConnectionManager for ConnectionManager<HM, RE, RD>
where
    HM: IHardwareMonitor + Send,
    RE: IRuleEngine + Send,
    RD: IRoutingDaemon + Send,
{
    async fn accept_application(&mut self, app_req: ApplicationRequestFormat) {
        self.application_requirements.lock().unwrap().push(app_req);
        // Send Connection Setup Request to the responder
    }
}

impl<HM, RE, RD> ConnectionManager<HM, RE, RD>
where
    HM: IHardwareMonitor + Send,
    RE: IRuleEngine + Send,
    RD: IRoutingDaemon + Send,
{
    /// Create connection manager
    ///
    pub fn new(
        hardware_monitor: Arc<Mutex<HM>>,
        rule_engine: Arc<Mutex<RE>>,
        routing_daemon: Arc<Mutex<RD>>,
        config_path: Option<&str>,
    ) -> Self {
        // Extract config from path
        let config = match config_path {
            Some(path) => CmConfig::from_path(path),
            None => CmConfig::from_path("DefaultSettings.toml"),
        };

        ConnectionManager {
            tcp_sockets: Arc::new(Mutex::new(HashMap::new())),
            active_connections: Arc::new(Mutex::new(HashMap::new())),
            pending_connections: Arc::new(Mutex::new(vec![])),
            performance_indicator: None,
            application_requirements: Arc::new(Mutex::new(vec![])),
            config,
            hardware_monitor,
            rule_engine,
            routing_daemon,
        }
    }

    cfg_initiator!(
        pub async fn boot(&mut self) {
            self.accept_application(&mut self);
            self.boot_tcp_listener();
        }
    );

    // // functions unique to repeater node
    // cfg_repeater!(
    //     pub async fn boot(&mut self) {
    //         self.boot_tcp_lister()
    //     }
    // );

    // // functions unique to responder node
    // cfg_responder!(
    //     pub async fn boot(&mut self) {
    //         // Get performance indicator
    //         self.request_performance_indicator()
    //     }

    //     async fn create_ruleset() {}
    // );

    pub async fn boot(&mut self) {
        self.get_performance_indicator();
        self.boot_tcp_listener().await;
    }

    // functions common for all the features
    async fn boot_tcp_listener(&self) {
        // Boot tcp listener and start listening
        let socket_addr = format!("{}:{}", self.config.host, self.config.port);
        let listener = TcpListener::bind(&socket_addr).await.unwrap();

        // keep listen to incoming request, response
        loop {
            let (client, _) = listener.accept().await.unwrap();
            let mut frame_reader = FramedRead::new(client, LengthDelimitedCodec::new());
            while let Some(frame) = frame_reader.next().await {
                match frame {
                    Ok(data) => {
                        // received data
                        self.handle_message(&data).await;
                    }
                    Err(err) => {
                        // received error
                        println!("error {:?}", err)
                    }
                }
            }
        }
    }

    fn get_performance_indicator(&mut self) {
        // Request performance indicator to hardware monitor
        if cfg!(test) {
            self.performance_indicator = Some(PerformanceIndicator::default());
        } else {
            // Fetch current performance indicator from HM
            self.performance_indicator = Some(
                self.hardware_monitor
                    .lock()
                    .unwrap()
                    .get_performance_indicator(),
            );
        }
    }

    async fn handle_message(&self, data: &BytesMut) {}
    /// An interface to the application
    /// The application manipulate this function to start the application
    /// When only the node type is initiator, this function can be executed
    ///
    async fn forward_connection_setup_request(&self) {
        // Find next hop
        let next_hop_socket_addr = if cfg!(test) {
            todo!("get next hop for testing")
        } else {
            self.routing_daemon.lock().unwrap().get_next_hop_interface()
        };
        // Send connection setup request to next hop
        // Check if there is an existing connection to the next hop or not
        if let Some(existing_connection) =
            self.tcp_sockets.lock().unwrap().get(&next_hop_socket_addr)
        {
            // Send connection setup request to the next hop
            // existing_connection.write_all(b"connection setup request").await.unwrap();
        } else {
            // Create a new connection to the next hop
            let mut stream = TcpStream::connect(next_hop_socket_addr).await.unwrap();
        }
    }

    /// Listen to incoming connection setup request
    /// This function wait for request from initiator
    ///
    async fn accept_connection_setup_request(&self) {}

    /// Reject to connection setup request
    /// Rejection conditon
    ///     1. ?
    async fn reject_connection_setup_request(&self) {}

    /// Listen to incoming connection setup response
    ///
    async fn accept_connection_setup_response(&self) {}

    /// Reject to incoming connection setup response
    /// and send back abort message back to responder
    async fn reject_connection_setup_response(&self) {}

    /// Listen to incoming connection setup reject
    ///
    async fn accept_connection_setup_request_reject(&self) {}

    async fn accept_connection_setup_response_reject(&self) {}

    async fn accept_ruleset_termination(&self) {}

    /// Listen to incoming LAU
    async fn accept_link_allocation_update() {}

    /// Listen to incoming Barrier
    ///
    async fn accept_barrier() {}
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::hardware_monitor::interface::MockIHardwareMonitor;
    use crate::routing_daemon::interface::MockIRoutingDaemon;
    use crate::rule_engine::interface::MockIRuleEngine;

    // Helper function to get
    fn get_cm_with_mock(
    ) -> ConnectionManager<MockIHardwareMonitor, MockIRuleEngine, MockIRoutingDaemon> {
        let mock_hardware_monitor = Arc::new(Mutex::new(MockIHardwareMonitor::default()));
        let mock_rule_engine = Arc::new(Mutex::new(MockIRuleEngine::default()));
        let mock_routing_daemon = Arc::new(Mutex::new(MockIRoutingDaemon::default()));
        ConnectionManager::new(
            mock_hardware_monitor,
            mock_rule_engine,
            mock_routing_daemon,
            None,
        )
    }
    // test for common function
    #[test]
    fn test_init() {
        let mock_hardware_monitor = Arc::new(Mutex::new(MockIHardwareMonitor::default()));
        let mock_rule_engine = Arc::new(Mutex::new(MockIRuleEngine::default()));
        let mock_routing_daemon = Arc::new(Mutex::new(MockIRoutingDaemon::default()));
        let connection_manager = ConnectionManager::new(
            mock_hardware_monitor,
            mock_rule_engine,
            mock_routing_daemon,
            None,
        );
        assert_eq!(connection_manager.config.port, 52244);
        assert_eq!(connection_manager.config.host, "0.0.0.0");
    }

    #[tokio::test]
    #[ignore = "This boots actual socket. Ignore in unittesting"]
    async fn test_boot() {
        let mut mock_cm = get_cm_with_mock();
        mock_cm.boot().await
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
    cfg_initiator!(
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
    );
}
