use serde::{ser::Serialize, Deserialize};

/// Message crate that all the other messages have to implement
/// T: Serialize and Deserializable object
// pub (crate) trait Message<'a, T: Serialize + Deserialize<'a>>{

// }
pub(crate) trait Message {
    
}

pub(crate) struct ConnectionSetupRequest {}

impl Message for ConnectionSetupRequest {}

pub(crate) struct ConnectionSetupResponse {}

impl Message for ConnectionSetupResponse {}

pub(crate) struct ConnectionSetupReject {}

impl Message for ConnectionSetupReject {}

pub(crate) struct LinkAllocationUpdate {}

impl Message for LinkAllocationUpdate {}

pub(crate) struct Barrier {}

impl Message for Barrier {}
