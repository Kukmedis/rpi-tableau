from cfg import bus
import sqlite3
import os

conn = sqlite3.connect(os.path.expanduser('~/data/tableau.db'))
cursor = conn.cursor()
create_table_statement = """
    CREATE TABLE IF NOT EXISTS counters (
    id integer PRIMARY KEY,
    name string UNIQUE NOT NULL,
    value integer NOT NULL
    );"""
cursor.execute(create_table_statement)


@bus.on('counter:set')
def set_counter(name, counter):
    insert_statement = "INSERT OR REPLACE INTO counters(name, value) VALUES(?, ?);"
    with conn:
        cur = conn.cursor()
        cur.execute(insert_statement, (name, counter))
    bus.emit('counter:updated', name, counter)


@bus.on('counter:increment')
def increment_counter(name):
    insert_statement = "INSERT OR IGNORE INTO counters(name, value) VALUES(?, 0);"
    with conn:
        cur = conn.cursor()
        cur.execute(insert_statement, name)

    update_statement = "UPDATE counters SET value = value + 1 WHERE name = ?;"
    with conn:
        cur = conn.cursor()
        cur.execute(update_statement, name)

    select_value_statement = "SELECT value FROM counters WHERE name = ?;"
    with conn:
        cur = conn.cursor()
        counter = cur.execute(select_value_statement, name).fetchone()

    bus.emit('counter:updated', name, counter)