from pydantic import BaseModel, Field


class ApplicationPerformanceRequest(BaseModel):
    minimum_fidelity: float = Field(
        0.0, ge=0.0, le=1.0, alias="Required fidelity for this application."
    )
    minimum_bell_pair_bandwidth: float = Field(
        0.0, ge=0.0, alias="Required bell pair andwidth for this application."
    )

    def __init__(self, minimum_fidelity, minimum_bell_pair_bandwidth):
        super().__init__()
        self.minimum_fidelity = minimum_fidelity
        self.minimum_bell_pair_bandwidth = minimum_bell_pair_bandwidth
