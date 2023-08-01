use mockall::automock;
use std::net::SocketAddr;

#[automock]
pub trait IRoutingDaemon {
    fn get_next_hop_interface(&self) -> SocketAddr;
}
