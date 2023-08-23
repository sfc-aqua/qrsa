from pydantic import BaseModel, Field


class MetaInfo(BaseModel):
    """
    A model for meta information
    """

    ip_address: str = Field(..., description="IP address of the node")
    hostname: str = Field(..., description="Hostname of the node")


class Config(BaseModel):
    """
    A model for input config
    """

    meta: MetaInfo = Field(..., description="Meta information of the node")
