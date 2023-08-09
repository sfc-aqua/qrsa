from typing import List
from pydantic import BaseModel, Field
from ruleset import RuleSet


class ConnectionSetupResponse(BaseModel):
    application_id: str = Field(
        ..., alias="Application Id corresponding to the connection id"
    )
    connection_id: str = Field(..., alias="Identifier for this connection")
    rulesets: List[RuleSet] = Field(..., alias="List of rulesets in this connection")
