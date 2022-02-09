import sqlite3

import psycopg2
from psycopg2.extras import DictCursor
from dotenv import dotenv_values

import load_from_sqlite

if __name__ == '__main__':
    config = dotenv_values(".env")
    dsl = {'dbname': config['dbname'], 'user': config['user'], 'password': config['password'], 'host': config['host'], 'port': config['port']}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite.load_from_sqlite(sqlite_conn, pg_conn)
    sqlite_conn.close()
            
