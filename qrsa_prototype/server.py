# from http.server import HTTPServer, BaseHTTPRequestHandler
import uvicorn
from fastapi import FastAPI
import socket


app = FastAPI()

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app=app, host=ip_address, port=8080)
