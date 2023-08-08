use serde::{Deserialize, Serialize};
use uuid::Uuid;

/// ApplicationId is used to identify which application is corresponding to which RuleSet
/// Initiator pass this id to responder and responder creates RuleSets and return them with this value
pub type ApplicationId = Uuid;

/// Ids for
pub type ConnectionId = Uuid;
