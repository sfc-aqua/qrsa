use serde::Deserialize;

#[derive(Deserialize)]
pub(crate) struct CmConfig {
    pub host: String,
    pub port: i64,
    pub num_thread: i64,
}
