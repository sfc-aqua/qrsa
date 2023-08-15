from typing import List
from pydantic import BaseModel, Field

from common.models.ruleset import RuleSet


class ConnectionSetupResponse(BaseModel):
    application_id: str = Field(
        ..., description="Application Id corresponding to the connection id"
    )
    connection_id: str = Field(..., description="Identifier for this connection")
    rulesets: List[RuleSet] = Field(
        ..., description="List of rulesets in this connection"
    )
