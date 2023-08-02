use crate::connection_manager::message::message::Message;

pub(crate) struct LinkAllocationUpdate {}

impl Message for LinkAllocationUpdate {
    fn get_destination(&self) -> std::net::IpAddr {
        unimplemented!()
    }
}
