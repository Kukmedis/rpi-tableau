import os
import db
import console

from flask import Flask, request, abort
from cfg import bus


__all__ = ['db', 'console']

app = Flask(__name__)
api_key = os.environ['API_KEY']


@app.route("/counters/<name>/<int:counter>", methods=['PUT'])
def set_counter(name, counter):
    validate_header()
    bus.emit('counter:set', name, counter)
    return "OK"


@app.route("/counters/<name>/inc", methods=['POST'])
def increment(name):
    validate_header()
    bus.emit('counter:increment', name)
    return "OK"


def validate_header():
    if not request.headers.get("api-key") or request.headers.get("api-key")[0] != api_key:
        abort(400)


if __name__ == '__main__':
    bus.emit('app:started')
    app.run(debug=False,host='0.0.0.0',port=80)