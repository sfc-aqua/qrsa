use mockall::automock;

#[automock]
pub trait IRoutingDaemon {
    fn get_next_hop_interface(&self);
}
