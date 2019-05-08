import os
import db
import console

from flask import Flask, request, abort
from cfg import bus


__all__ = ['db', 'console']

app = Flask(__name__)
api_key = os.environ['API_KEY']


def init():
    bus.emit('app:started', threads=True)


@app.route("/counters/<name>/<int:counter>", methods=['PUT'])
def set_counter(name, counter):
    validate_header()
    bus.emit('counter:set', name, counter, threads=True)
    return "OK"


@app.route("/counters/<name>/inc", methods=['POST'])
def increment(name):
    validate_header()
    bus.emit('counter:increment', name, threads=True)
    return "OK"


def validate_header():
    if not request.headers.get("api-key") or request.headers.get("api-key") != api_key:
        abort(400)


init()


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)