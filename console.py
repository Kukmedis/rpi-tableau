import threading
from time import sleep

import db
from cfg import bus


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
            print(counter)
        last_displayed = counter
        sleep(1)