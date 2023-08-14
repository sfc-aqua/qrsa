#!/bin/sh

# work dir /usr/app
# Since the current volume mount shares .venv over the different containers, rye returns
# installation error. Instead of using rye in the container, we use venv directly.
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.lock
python3 server.py

