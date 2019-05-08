from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=90)


def draw_text(val):
    with canvas(device) as draw:
        text(draw, (0, 0), val, fill="white")