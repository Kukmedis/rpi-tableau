import threading
from time import sleep

from luma.core.interface.serial import spi, noop
from luma.core.legacy import text
from luma.core.render import canvas
from luma.led_matrix.device import max7219

import db
from cfg import bus

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=90)


def draw_text(val):
    with canvas(device) as draw:
        text(draw, (0, 0), val, fill="white")


@bus.on('app:started')
def start():
    thread = threading.Thread(target=loop)
    thread.daemon = True
    thread.start()


def loop():
    last_displayed = None
    while True:
        counter = db.get_counter("tx")
        if counter != last_displayed:
            draw_text(str(counter))
        last_displayed = counter
        sleep(1)
