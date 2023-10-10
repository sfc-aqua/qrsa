from enum import Enum
import subprocess
from typing import Optional

BASE_CMD = "docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock gaiaadm/pumba netem".split(
    " "
)


class PumbaDelayDistribution(Enum):
    Uniform = "uniform"
    Normal = "normal"
    Pareto = "pareto"
    ParetoNormal = "paretonormal"


def delay(
    container: str,
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


def loss(container: str, target_ip):
    cmd = BASE_CMD + [
        "--duration",
        "999h",
        "loss",
        container,
        "--target",
        target_ip,
        "--percent",
        "100",
    ]
    print(cmd)
    return subprocess.run(cmd)
