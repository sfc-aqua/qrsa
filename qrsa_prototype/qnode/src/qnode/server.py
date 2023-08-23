import socket
import yaml
from fastapi import FastAPI

from qnode.endpoints import router
from qnode.containers import Container
from common.models.configs.config import Config


def create_server() -> FastAPI:
    config = generate_config()
    container = Container()
    container.config.from_dict(config)

    app = FastAPI()
    app.container = container
    app.include_router(router)
    return app


def generate_config() -> Config:
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    with open("./config/default_config.yml", "r") as f:
        config = yaml.safe_load(f)

    # update default config with current ip address
    config["meta"]["ip_address"] = ip_address
    config["meta"]["hostname"] = hostname
    return Config(**config)
