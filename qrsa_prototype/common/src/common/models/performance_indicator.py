from pydantic import BaseModel, Field


class PerformanceIndicator(BaseModel):
    """
    Performance indicator that is used to construct RuleSet
    The contents of this message is still under discussion
    """

    local_op_fidelity: float = Field(..., description="Local operation fidelity")
