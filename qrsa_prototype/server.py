import socket
import uvicorn
from typing import Any
from fastapi import FastAPI

from common.models.connection_setup_request import ConnectionSetupRequest



app = FastAPI()

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


@app.get("/heat_beat")
def heart_beat() -> dict:
    return {"message": "Alive"}


@app.post("/connection_setup_request")
def handle_connection_setup_request(request: ConnectionSetupRequest) -> dict:
    # Deserialize connection setup request
    print(request)

    # Add performance indicator to the request

    # Serialize connection setup request again

    # Send connection setup request to next hop
    return {"message": "Hello World", "contents": str(request)}


if __name__ == "__main__":
    uvicorn.run("server:app", host=ip_address, port=8080, reload=True)
