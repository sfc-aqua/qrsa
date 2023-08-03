use std::net::IpAddr;

/// Message trait that defines an interface for each message structure
pub(crate) trait Message {
    fn get_source(&self) -> IpAddr;
    fn get_destination(&self) -> IpAddr;
}
