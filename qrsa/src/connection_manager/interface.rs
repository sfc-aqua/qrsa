use async_trait::async_trait;
use mockall::automock;
use std::net::IpAddr;

use crate::common::application_request_format::ApplicationRequestFormat;

#[automock]
#[async_trait]
pub trait IConnectionManager {
    async fn accept_application(&mut self, destination: IpAddr, app_req: ApplicationRequestFormat);
}
