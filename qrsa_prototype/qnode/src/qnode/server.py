import socket
from fastapi import FastAPI

from .endpoints import router
from .containers import Container


def create_server() -> FastAPI:
    config = generate_config()
    container = Container()
    container.config.from_dict(config)

    app = FastAPI()
    app.container = container
    app.include_router(router)
    return app


def generate_config() -> None:
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    config = {"ip_address": ip_address}
    return config


# app = create_server()
