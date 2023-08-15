import socket
import uvicorn
from typing import Annotated
from fastapi import FastAPI, Depends

from common.models.connection_setup_request import ConnectionSetupRequest
from common.models.connection_setup_response import ConnectionSetupResponse
from common.models.connection_setup_reject import ConnectionSetupReject

from connection_manager.connection_manager import ConnectionManager

app = FastAPI()

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


@app.get("/heat_beat")
async def heart_beat() -> dict:
    return {"message": "Alive"}


@app.post("/connection_setup_request")
async def handle_connection_setup_request(
    request: ConnectionSetupRequest,
    connection_manager: Annotated[ConnectionManager, Depends(ConnectionManager)],
) -> dict:
    """
    Experimental function to handle connection setup requests
    :param request: ConnectionSetupRequest
    :return: dict

    In the future, we may want to communicate over a different protocol
    as they are implemented on routers or repeaters.
    """
    if hostname == request.header.dst:
        # This node is the final destination
        # Create RuleSet
        rulesets = connection_manager.create_rule_set(request)
        print(rulesets)
        pass
    # Add performance indicator to the request

    # Serialize connection setup request again

    # Send connection setup request to next hop
    return {"message": "Hello World", "contents": str(request)}


@app.post("/connection_setup_response")
async def handle_connection_setup_response(response: ConnectionSetupResponse):
    return {"message": "Received connection setup response"}


@app.post("/connection_setup_reject")
async def handle_connection_setup_reject(reject: ConnectionSetupReject):
    return {"message": "Received connection setup reject"}


@app.post("/lau_update")
async def handle_lau_update():
    return {"message": "Received LAU update"}


@app.post("/barrier")
async def handle_barrier():
    return {"message": "Received barrier"}


def main():
    uvicorn.run("server:app", host=ip_address, port=8080, reload=True)


if __name__ == "__main__":
    main()
