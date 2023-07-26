use mockall::automock;

#[automock]
pub trait IRoutingDaemon {
    fn get_interface_info();
}
