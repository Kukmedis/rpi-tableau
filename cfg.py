import os

from event_bus import EventBus


__all__ = ['db', 'console']
bus = EventBus()
db_location = os.path.expanduser('~/data/tableau.db')

print("DB Location: " + db_location)