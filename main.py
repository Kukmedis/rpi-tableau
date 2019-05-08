import os

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text
from flask import Flask, request, abort
from tinydb import TinyDB, Query

db = TinyDB('/data/tableau-db.json')
app = Flask(__name__)
api_key = os.environ['API_KEY']

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=90)


def draw_text(val):
    with canvas(device) as draw:
        text(draw, (0, 0), val, fill="white")


@app.route("/counter/<int:counter>", methods=['PUT'])
def set_counter(counter):
    validate_header()
    db.upsert({'key': 'counter', 'number': counter}, Query().key == 'counter')
    draw_text(str(counter))
    return "OK"


@app.route("/counter/inc", methods=['POST'])
def increment():
    validate_header()
    counter = db.get(Query().key == 'counter')
    number = counter.number + 1 if counter is not None else 1
    draw_text(str(number))
    db.upsert({'key': 'counter', 'number': number}, Query().key == 'counter')
    return "OK"


def validate_header():
    if not request.headers.get("api-key") or request.headers.get("api-key")[0] != api_key:
        abort(400)


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')