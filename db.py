from cfg import bus, db_location
import sqlite3


def init():
    create_table_statement = """
        CREATE TABLE IF NOT EXISTS counters (
        id integer PRIMARY KEY,
        name string UNIQUE NOT NULL,
        value integer NOT NULL
        );"""
    with sqlite3.connect(db_location) as conn:
        conn.execute(create_table_statement)


@bus.on('counter:set')
def set_counter(name, counter):
    insert_statement = "INSERT OR REPLACE INTO counters(name, value) VALUES(?, ?);"
    with sqlite3.connect(db_location) as conn:
        conn.execute(insert_statement, (name, counter))
    bus.emit('counter:updated', name, counter, threads=True)


@bus.on('counter:increment')
def increment_counter(name):
    with sqlite3.connect(db_location) as conn:
        insert_statement = "INSERT OR IGNORE INTO counters(name, value) VALUES(?, 0);"
        conn.execute(insert_statement, [name])
        update_statement = "UPDATE counters SET value = value + 1 WHERE name = ?;"
        conn.execute(update_statement, [name])
        select_value_statement = "SELECT value FROM counters WHERE name = ?;"
        counter = conn.execute(select_value_statement, [name]).fetchone()[0]
    bus.emit('counter:updated', name, counter, threads=True)


init()