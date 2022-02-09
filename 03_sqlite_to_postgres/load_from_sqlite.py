import sqlite3
from psycopg2.extensions import connection as _connection
from sqlite_postgres_module import PostgresSaver, SQLiteLoader


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)
    
    count = 1
    offset = 0
    BATCH_SIZE = 500
    while count > 0:
        data = sqlite_loader.load_movies(offset, BATCH_SIZE)
        count = 0
        for listElem in data:
            count += len(data[listElem])
        offset += BATCH_SIZE
        postgres_saver.save_all_data(data)