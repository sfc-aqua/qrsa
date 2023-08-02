use crate::common::application_request_format::ApplicationRequestFormat;
use crate::connection_manager::connection::id::ApplicationId;
use crate::{
    common::performance_indicator::PerformanceIndicator,
    connection_manager::message::message::Message,
};
use serde::{Deserialize, Serialize};
use std::net::IpAddr;

#[derive(Serialize, Deserialize)]
pub(crate) struct ConnectionSetupRequest {
    destination: IpAddr,
    application_id: ApplicationId,
    application_requirement: ApplicationRequestFormat,
    performance_indicator: PerformanceIndicator,
}

impl Message for ConnectionSetupRequest {
    fn get_destination(&self) -> IpAddr {
        self.destination
    }
}
