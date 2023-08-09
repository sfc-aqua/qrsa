from typing import List
from pydantic import BaseModel, Field


class ActionClause(BaseModel):
    pass


class ConditionClause(BaseModel):
    pass


class Action(BaseModel):
    clauses: List[ActionClause] = Field(..., alias="List of clauses in this action")


class Condition(BaseModel):
    clauses: List[ConditionClause] = Field(
        ..., alias="List of clauses in this condition"
    )


class Rule(BaseModel):
    rule_id: int = Field(..., alias="Identifier for this rule")


class Stage(BaseModel):
    stage_id: int = Field(..., alias="Identifier for this stage")
    rules: List[Rule] = Field(..., alias="List of rules in this stage")


class RuleSet(BaseModel):
    ruleset_id: str = Field(..., alias="Identifier for this ruleset")
    stages: List[Stage] = Field(..., alias="List of stages in this ruleset")
