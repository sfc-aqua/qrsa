use async_trait::async_trait;
use mockall::automock;

use crate::common::application_request_format::ApplicationRequestFormat;

#[automock]
#[async_trait]
pub trait IConnectionManager {
    async fn accept_application(&mut self, app_req: ApplicationRequestFormat);
}
