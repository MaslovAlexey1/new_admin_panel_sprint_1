import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor


class SQLiteLoader:
    def __init__(self, conn):
        self.cursor = conn.cursor()

    def load_movies(self):
        tables = ['genre', 'person', 'film_work',
                  'genre_film_work', 'person_film_work']
        data = {}
        for table in tables:
            sql = "SELECT * from {}".format(table)
            data[table] = self.cursor.execute(sql).fetchall()
        return data


class PostgresSaver:
    def __init__(self, conn):
        self.cursor = conn.cursor()

    def save_all_data(self, data):
        args = ','.join(self.cursor.mogrify("(%s, %s, %s, %s, %s)", item).decode() for item in data['genre'])
        self.cursor.execute(f"""
        INSERT INTO content.genre
        (id, name, description, created_at, updated_at)
        VALUES {args}
        ON CONFLICT (id) DO UPDATE SET  name=EXCLUDED.name,
                                        description=EXCLUDED.description,
                                        created_at=EXCLUDED.created_at,
                                        updated_at=EXCLUDED.updated_at

        """)
        # print(data['person'])

        args = ','.join(self.cursor.mogrify("(%s, %s, %s, %s, %s)", item).decode() for item in data['person'])
        self.cursor.execute(f"""
        INSERT INTO content.person
        (id, full_name, birth_date, created_at, updated_at)
        VALUES {args}
        ON CONFLICT (id) DO UPDATE SET  full_name=EXCLUDED.full_name,
                                        birth_date=EXCLUDED.birth_date,
                                        created_at=EXCLUDED.created_at,
                                        updated_at=EXCLUDED.updated_at

        """)

        args = ','.join(self.cursor.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", item).decode() for item in data['film_work'])
        self.cursor.execute(f"""
        INSERT INTO content.film_work
        (id, title, description, creation_date, certificate, file_path, rating, type, created_at, updated_at)
        VALUES {args}
        ON CONFLICT (id) DO UPDATE SET  title=EXCLUDED.title,
                                        description=EXCLUDED.description,
                                        creation_date=EXCLUDED.creation_date,
                                        certificate=EXCLUDED.certificate,
                                        file_path=EXCLUDED.file_path,
                                        rating=EXCLUDED.rating,
                                        type=EXCLUDED.type,
                                        created_at=EXCLUDED.created_at,
                                        updated_at=EXCLUDED.updated_at

        """)

        args = ','.join(self.cursor.mogrify("(%s, %s, %s, %s)", item).decode() for item in data['genre_film_work'])
        self.cursor.execute(f"""
        INSERT INTO content.genre_film_work
        (id, film_work_id, genre_id, created_at)
        VALUES {args}
        ON CONFLICT (id) DO UPDATE SET  film_work_id=EXCLUDED.film_work_id,
                                        genre_id=EXCLUDED.genre_id,
                                        created_at=EXCLUDED.created_at

        """)

        args = ','.join(self.cursor.mogrify("(%s, %s, %s, %s, %s)", item).decode() for item in data['person_film_work'])
        self.cursor.execute(f"""
        INSERT INTO content.person_film_work
        (id, film_work_id, person_id, role, created_at)
        VALUES {args}
        ON CONFLICT (id) DO UPDATE SET  film_work_id=EXCLUDED.film_work_id,
                                        person_id=EXCLUDED.person_id,
                                        role=EXCLUDED.role,
                                        created_at=EXCLUDED.created_at

        """)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)
    # print(data)


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
