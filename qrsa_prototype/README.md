# QRSA prototype

This project is a python prototype of deployable Quantum Routing Software Architecture.

## Introduction
The prototype is implemented in python which might not be the best choice for real deployment. However, it is good enough to demonstrate the idea of QRSA and clarify the requirements.

## Tools and Environments
This project requires following tools and environments.

### Docker

In order to run the prototype, you need to install docker. Please refer to [Docker Installation](https://docs.docker.com/engine/installation/) for details.

Docker container forms a docker network and they are able to communicate with each other.

### Rye

[Rye](https://rye-up.com/guide/installation/) is a python pakage and virtual environment manager. You don't need manual installation since it's included in the docker image.


### Python

The supported python version is 3.11 or above.

## Setup

### Build Docker Images

Run following command to build docker images.

```bash
$ docker-compose build
```

### Run Docker Containers

Run following command to run docker containers.

```bash
$ docker-compose up -d
```

You can see the containers are running through docker desktop dash board or `docker ps`

### Enter Container

To attach to a running container, use the docker exec command.

```bash
$ docker exec -it <container id> bash
```

`<container id>` is the name of container that you can find from `docker ps`.

If you're using Visual Studio Code, you can use the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension to open the project folder in a container. Install docker extension in vscode and attach to the running container.

### Run task
In order to start the connection setup process, you need to run the following command in the container.

```bash
rye run python qnode/src/qnode/bootstrap.py 
```

The container you hit this command must be an initiator. 

## Files and Directories
qrsa prototype is composed of the following components.

- `common`: A module that contains models of messages and some utility functions. Packages used across different components should be implemented here.
  - `models`: Pydantic mdoels of messages
  - `log`: JSON logger
  - `type_utils.py`: Provide type aliases.

- `qnode`: A module that contains the implementation of qnode. It includes the implementation of qnode, qnode manager, and qnode controller.
  - `bootstrap.py`: Issue a request to start connection setup.
  - `container.py`: Dependency injection container. This container provides singleton instances of qrsa components and configuration.
  - `server.py`: Prepare fastapi app.
  - `endpoints.py`: Defines message handler endpoints in FastAPI. The qrsa components are injected independently.
  - `connection_manager`: Connection Manager is responsible for managing connections with other qnodes. It provides APIs for qnode to send messages to other qnodes.
  - `hardware_monitor`: Hardware Manager monitors link status.
  - `routing_daemon`: A deaemon process that listen to the routing information changes.
  - `rule_engine`: Rule Engine receives RuleSet from the responder and execute RuleSet.
  - `real_time_controller`: Real Time Controller provides interfaces to hardware components.

- `src`: Instantiate server and run it.
  - `qnode/main.py`: Instantiate qnode server and run it on uvicorn.

- `tests`: pytest test cases.

## Formatting
Python [black module](https://github.com/psf/black) is used for formatting. You can run following command to format the code.

```bash
rye run black .
```


## Testing
Tests are implmented in pytest. Tests can be done through following command.
    
```bash
rye run pytest
```

If you are using vscode, python extention provides a test explorer. You can run tests through the test explorer.
