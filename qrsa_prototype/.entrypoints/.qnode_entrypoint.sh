#!/bin/sh

# work dir /usr/app
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.lock
python3 server.py