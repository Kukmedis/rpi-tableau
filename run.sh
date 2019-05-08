#!/usr/bin/env bash

export FLASK_APP=api
./pi-tableau-venv/bin/waitress-serve --port 80 --call 'api:create_app'