# from http.server import HTTPServer, BaseHTTPRequestHandler
import uvicorn
from fastapi import FastAPI
import socket


app = FastAPI()

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


@app.get("/heat_beat")
async def heart_beat() -> dict:
    return {"message": "Hello World"}


@app.post("/connection_setup_request")
async def handle_connection_setup_request(request):
    # Deserialize connection setup request

    # Add performance indicator to the request

    # Serialize connection setup request again

    # Send connection setup request to next hop
    pass


if __name__ == "__main__":
    uvicorn.run(app=app, host=ip_address, port=8080)
