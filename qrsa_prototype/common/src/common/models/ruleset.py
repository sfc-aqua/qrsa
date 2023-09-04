from typing import List
from pydantic import BaseModel, Field


class ActionClause(BaseModel):
    pass


class ConditionClause(BaseModel):
    pass


class Action(BaseModel):
    clauses: List[ActionClause] = Field(
        ..., description="List of clauses in this action"
    )


class Condition(BaseModel):
    clauses: List[ConditionClause] = Field(
        ..., description="List of clauses in this condition"
    )


class Rule(BaseModel):
    rule_id: int = Field(..., description="Identifier for this rule")


class Stage(BaseModel):
    stage_id: int = Field(..., description="Identifier for this stage")
    rules: List[Rule] = Field(..., description="List of rules in this stage")


class RuleSet(BaseModel):
    ruleset_id: str = Field(..., description="Identifier for this ruleset")
    stages: List[Stage] = Field(..., description="List of stages in this ruleset")
