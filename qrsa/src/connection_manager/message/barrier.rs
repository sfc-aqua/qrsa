use crate::connection_manager::message::message::Message;
use std::net::IpAddr;

pub(crate) struct Barrier {}

impl Message for Barrier {
    fn get_source(&self) -> IpAddr {
        unimplemented!()
    }
    fn get_destination(&self) -> IpAddr {
        unimplemented!()
    }
}
