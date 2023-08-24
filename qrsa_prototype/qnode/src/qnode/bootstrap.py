from ipaddress import IPv4Address

from common.models.app_performance_requirement import ApplicationPerformanceRequirement
from qnode.server import create_server

if __name__ == "__main__":
    # Create a client
    (_, client) = create_server()

    # Application will give this information to CM
    app_req = {
        "minimum_fidelity": 0.9,
        "minimum_bell_pair_bandwidth": 100,
    }

    client.send_connection_setup_request(
        IPv4Address("172.18.0.4"), ApplicationPerformanceRequirement(**app_req)
    )
