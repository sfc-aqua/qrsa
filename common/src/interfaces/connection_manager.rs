use async_trait::async_trait;
use mockall::automock;

use crate::models::application_request_format::ApplicationRequestFormat;

#[automock]
#[async_trait]
pub trait IConnectionManager {
    #[cfg(feature = "initiator")]
    async fn accept_application(&mut self, app_req: ApplicationRequestFormat);
}
