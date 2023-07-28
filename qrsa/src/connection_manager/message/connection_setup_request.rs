use crate::connection_manager::connection::id::ApplicationId;
use crate::{
    common::performance_indicator::PerformanceIndicator,
    connection_manager::message::message::Message,
};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub(crate) struct ConnectionSetupRequest {
    application_id: ApplicationId,
    performance_indicator: PerformanceIndicator,
}

impl Message for ConnectionSetupRequest {}
