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
    source: IpAddr,
    destination: IpAddr,
    application_id: ApplicationId,
    application_requirement: ApplicationRequestFormat,
    performance_indicator: PerformanceIndicator,
}

impl ConnectionSetupRequest {
    pub fn new(
        source: IpAddr,
        destination: IpAddr,
        application_id: ApplicationId,
        application_requirement: ApplicationRequestFormat,
        performance_indicator: PerformanceIndicator,
    ) -> Self {
        ConnectionSetupRequest {
            source,
            destination,
            application_id,
            application_requirement,
            performance_indicator,
        }
    }
}

impl Message for ConnectionSetupRequest {
    fn get_source(&self) -> IpAddr {
        self.source
    }
    fn get_destination(&self) -> IpAddr {
        self.destination
    }
}
