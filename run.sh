#!/usr/bin/env bash

export FLASK_APP=api
./pi-tableau-venv/bin/waitress-serve --call 'api:create_app'