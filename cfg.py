import os

from event_bus import EventBus

bus = EventBus()
db_location = os.path.expanduser('~/data/tableau.db')