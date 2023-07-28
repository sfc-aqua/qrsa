pub mod connection_manager {
    pub mod config {
        pub(crate) mod model;
    }
    pub(crate) mod connection {
        pub mod id;
        pub mod connection;
    }
    pub(crate) mod message {
        pub mod barrier;
        pub mod connection_setup_reject;
        pub mod connection_setup_request;
        pub mod connection_setup_response;
        pub mod link_allocation_update;
        pub mod message;
    }
    pub(crate) mod ruleset_factory {
        pub(crate) mod ruleset_factory;
    }

    pub(crate) mod macros {
        pub(crate) mod cfg;
    }
    pub mod connection_manager;
    pub(crate) mod error;
    pub(crate) mod interface;

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
