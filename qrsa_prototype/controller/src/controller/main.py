import os
import subprocess
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from controller.api import api


client_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../client/"))
client_build_path = os.path.join(client_dir, "build")
if not os.path.exists(client_build_path):
    subprocess.run("npm ci", shell=True, cwd=client_dir)
    subprocess.run("npm run build", shell=True, cwd=client_dir)

app = FastAPI()
app.mount("/api", api)
app.mount("/", StaticFiles(directory=client_build_path, html=True))
