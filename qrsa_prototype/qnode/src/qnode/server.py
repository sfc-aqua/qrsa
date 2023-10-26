import logging
import socket
from typing import Any
import yaml
import aiohttp
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from qnode.endpoints import router
from qnode.containers import Container
from common.models.configs import Config


def create_server() -> FastAPI:
    config = generate_config()
    container = Container()
    # Managing config in pydantic model would be cleaner, but currently
    # there is a bug so that we cannot use from_pydantic() method in this version
    # https://github.com/ets-labs/python-dependency-injector/issues/726
    container.config.from_dict(config.model_dump())

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

class EndpointFilter(logging.Filter):
    def __init__(
        self,
        path: str,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._path = path

    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find(self._path) == -1

uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.addFilter(EndpointFilter(path="/status"))