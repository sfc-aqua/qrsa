pub mod connection_manager {
    pub mod config {
        pub(crate) mod config;
    }
    pub(crate) mod connection {
        pub mod connection;
    }
    pub mod connection_manager;
    pub(crate) mod error;
    pub(crate) mod interface;
    pub(crate) mod message;
    pub(crate) mod ruleset_factory;

    use error::ConnectionManagerError;
    type IResult<T> = Result<T, ConnectionManagerError>;
}

pub mod realtime_controller {
    pub mod interface;
    pub mod realtime_controller;
}

pub mod hardware_monitor {
    pub mod hardware_monitor;
    pub mod interface;
}

pub mod routing_daemon {
    pub mod interface;
    pub mod routing_daemon;
}

pub mod rule_engine {
    pub mod interface;
    pub mod la_policy_manager;
    pub mod resource_allocator;
    pub mod rule_engine;
    pub mod runtime;
    pub mod scheduler;
}

pub mod common {
    pub mod application_request_format;
    pub mod link_allocation_policy;
    pub mod performance_indicator;
    pub mod resources;
    pub mod ruleset;
}
