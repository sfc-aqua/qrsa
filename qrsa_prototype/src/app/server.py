import socket
import uvicorn
from fastapi import FastAPI

from endpoints import router
from containers import Container

app = FastAPI()


def create_server() -> FastAPI:
    container = Container()

    app = FastAPI()
    app.container = container
    app.include_router(router)
    return app


app = create_server()


if __name__ == "__main__":
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    uvicorn.run("server:app", host=ip_address, port=8080, reload=True)
