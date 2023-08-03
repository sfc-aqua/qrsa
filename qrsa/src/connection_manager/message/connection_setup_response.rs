use crate::connection_manager::message::message::Message;
pub(crate) struct ConnectionSetupResponse {}

impl Message for ConnectionSetupResponse {
    fn get_source(&self) -> std::net::IpAddr {
        unimplemented!()
    }
    fn get_destination(&self) -> std::net::IpAddr {
        unimplemented!()
    }
}
