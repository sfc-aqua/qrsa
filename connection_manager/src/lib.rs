pub(crate) mod config;
pub(crate) mod connection;
pub mod connection_manager;
pub(crate) mod error;
pub(crate) mod message;
pub(crate) mod ruleset_factory;

use error::ConnectionManagerError;
type IResult<T> = Result<T, ConnectionManagerError>;
