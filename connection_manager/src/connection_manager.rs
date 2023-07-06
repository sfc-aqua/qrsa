

/// A main struct for Connection manager
/// 
pub struct ConnectionManager{}

impl ConnectionManager{
    pub fn new(){

    }

    /// An interface to the application
    /// The application manipulate this function to start the application
    /// When only the node type is initiator, this function can be executed
    /// 
    /// 
    pub fn accept_application(){

    }

    /// Listen to incoming connection setup request
    /// This function wait for request from initiator
    /// 
    pub async fn listen_to_connection_setup_request(){

    }

    /// Listen to incoming connection setup response
    /// 
    pub async fn listen_to_connection_setup_response(){

    }

    /// Listen to incoming connection setup reject
    /// 
    pub async fn listen_to_connection_setup_reject(){

    }

    /// Listen to incoming LAU
    pub async fn listen_to_link_allocation_update(){

    }

    /// Listen to incoming Barrier
    /// 
    pub async fn listen_to_barrier(){

    }
}