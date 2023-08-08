use mockall::automock;
use std::net::{IpAddr, SocketAddr};

#[automock]
pub trait IRoutingDaemon {
    fn get_next_hop_interface(&self, destination: IpAddr) -> SocketAddr;
}
