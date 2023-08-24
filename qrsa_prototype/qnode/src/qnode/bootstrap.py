import aiohttp
import asyncio
import socket
from common.models.application_bootstrap import ApplicationBootstrap
from common.models.app_performance_requirement import (
    ApplicationPerformanceRequirement,
)


async def start_connection_setup():
    ip_address = socket.gethostbyname(socket.gethostname())
    destination = "172.18.0.4"

    app_req = ApplicationPerformanceRequirement(
        **{
            "minimum_fidelity": 0.9,
            "minimum_bell_pair_bandwidth": 10,
        }
    )
    # Application will give this information to CM
    app_bootstrap_json = ApplicationBootstrap(
        **{
            "destination": destination,
            "application_performance_requirement": app_req,
        }
    ).model_dump_json()

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"http://{ip_address}:8080/start_connection_setup",
            data=app_bootstrap_json,
            headers={"Content-Type": "application/json"},
        ) as resp:
            print(await resp.read())


if __name__ == "__main__":
    asyncio.run(start_connection_setup())
