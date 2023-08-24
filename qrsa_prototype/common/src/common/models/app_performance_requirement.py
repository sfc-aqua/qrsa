from pydantic import BaseModel, Field


class ApplicationPerformanceRequirement(BaseModel):
    minimum_fidelity: float = Field(
        0.0, ge=0.0, le=1.0, description="Required fidelity for this application."
    )
    minimum_bell_pair_bandwidth: int = Field(
        0, ge=0.0, description="Required bell pair andwidth for this application."
    )
