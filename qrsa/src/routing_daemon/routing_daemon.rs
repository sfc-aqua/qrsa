use std::net::SocketAddr;

use super::interface::IRoutingDaemon;

/// A struct that is responsible for
///  creating routing table
///  updating routing table
///
/// This struct is a Rust wrapper for FRRouting https://github.com/FRRouting/frr
pub struct RoutingDaemon {}

impl RoutingDaemon {
    pub fn new() {}

    pub fn get_interface_for_next_hop() {}
}

impl IRoutingDaemon for RoutingDaemon {
    fn get_next_hop_interface(&self) -> SocketAddr {
        if cfg!(test) {
            SocketAddr::from(([127, 0, 0, 1], 8080))
        } else {
            SocketAddr::from(([127, 0, 0, 1], 8080))
        }
    }
}
