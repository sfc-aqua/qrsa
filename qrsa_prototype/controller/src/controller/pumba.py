from enum import Enum
import subprocess
from typing import Optional

BASE_CMD = "docker run -it --rm  -v /var/run/docker.sock:/var/run/docker.sock gaiaadm/pumba netem".split(
    " "
)


class PumbaDelayDistribution(Enum):
    Uniform = "uniform"
    Normal = "normal"
    Pareto = "pareto"
    ParetoNormal = "paretonormal"


async def delay(
    id,
    time: float,
    jitter: float,
    correlation: float,
    distribution: Optional[PumbaDelayDistribution],
):
    return subprocess.run(
        BASE_CMD
        + [
            "delay",
            "--target",
            id,
            "--jitter",
            jitter,
            "--correlation",
            correlation,
            "--distribution",
            distribution,
        ]
    )
