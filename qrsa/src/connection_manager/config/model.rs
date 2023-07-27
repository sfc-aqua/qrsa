use config::Config;
use serde::Deserialize;

#[derive(Deserialize, Default, Debug)]
pub(crate) struct CmConfig {
    pub host: String,
    pub port: i64,
}

impl CmConfig {
    pub fn from_path(config_path: &str) -> Self {
        let config = Config::builder()
            .add_source(config::File::with_name(config_path))
            .build()
            .unwrap_or_else(|e| panic!("Failed to build config {:#?}", e));

        config
            .get::<CmConfig>("connection_manager")
            .unwrap_or_else(|dee| panic!("Failed to deserialize config into a model. {}", dee))
    }
}
