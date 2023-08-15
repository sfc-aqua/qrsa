import socket
import uuid
import requests
import ipaddress
from typing import Union, List, Annotated
from ipaddress import IPv4Address, IPv6Address
from fastapi import FastAPI, Depends

from common.models.connection_setup_request import ConnectionSetupRequest
from common.models.application_performance_request import ApplicationPerformanceRequest

from hardware_monitor.hardware_monitor import HardwareMonitor

app = FastAPI()

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


class QRSAClient:
    def __init__(self):
        self.pending_connection: List[str] = []

    # Application will use this function to start entire connection setup process
    def send_connection_setup_request(
        self,
        destination: Union[IPv4Address, IPv6Address],
        application_perofrmance_request: ApplicationPerformanceRequest,
        hardware_monitor: Annotated[HardwareMonitor, Depends(HardwareMonitor)],
    ):
        # Generate random application id
        application_id = str(uuid.uuid4())
        # Get the latest hardware perofrmance indicator
        performance_indicator = hardware_monitor.get_performance_indicator()
        # Create connection setup request
        csr_contents = {
            "header": {
                "src": ipaddress.ip_address(ip_address),
                "dst": destination,
            },
            "application_id": application_id,
            "application_performance_request": application_perofrmance_request,
            "performance_indicators": [performance_indicator],
        }

        csr = ConnectionSetupRequest(**csr_contents)

        # TODO: Get next hop from routing table
        next_hop = IPv4Address("172.18.0.3")
        # Serialize connection setup request
        csr_json = csr.model_dump_json()
        requests.post(
            f"http://{next_hop}:8080/connection_setup_request",
            data=csr_json,
            headers={"Content-Type": "application/json"},
        )


if __name__ == "__main__":
    client = QRSAClient()

    # Application will give this information to CM
    app_req = {
        "minimum_fidelity": 0.9,
        "minimum_bell_pair_bandwidth": 100,
    }

    client.send_connection_setup_request(
        IPv4Address("172.18.0.3"), ApplicationPerformanceRequest(**app_req)
    )
