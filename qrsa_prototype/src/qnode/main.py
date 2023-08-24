import socket
import uvicorn

from qnode import server

app, _ = server.create_server()


def main():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    uvicorn.run("main:app", host=ip_address, port=8080, reload=True)


if __name__ == "__main__":
    main()
