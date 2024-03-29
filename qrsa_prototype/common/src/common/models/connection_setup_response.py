from pydantic import BaseModel, Field

from common.models.ruleset import RuleSet
from common.models.header import Header


class ConnectionSetupResponse(BaseModel):
    """
    Connection Setup Response carries rulesets to intermediate quantum repeaters.
    Unlike ConnectionSetupRequest, the message may not go along a original path
    so one response message is created for one intermediate repeater.
    """

    header: Header = Field(..., description="Header")
    application_id: str = Field(
        ..., description="Application Id corresponding to the connection id"
    )
    connection_id: str = Field(..., description="Identifier for this connection")
    ruleset: RuleSet = Field(..., description="List of rulesets in this connection")
