use mockall::automock;

#[automock]
pub trait RealTimeController {
    fn start_link_generation(&self);
    fn schedule_instruction(&self);
}
