use serde::{ser::Serialize, Deserialize};

/// Message crate that all the other messages have to implement
/// T: Serialize and Deserializable object
pub (crate) trait Message<'a, T: Serialize + Deserialize<'a>>{

}