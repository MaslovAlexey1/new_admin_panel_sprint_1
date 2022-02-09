class SQLiteLoader:
    def __init__(self, conn):
        self.cursor = conn.cursor()

    def load_movies(self, offset, max_row_count):
        tables = ['genre', 'person', 'film_work',
                  'genre_film_work', 'person_film_work']
        data = {}
        for table in tables:
            sql = "SELECT * from {} order by created_at limit {}, {}".format(table, offset, max_row_count)
            data[table] = self.cursor.execute(sql).fetchall()
        return data


class PostgresSaver:
    def __init__(self, conn):
        self.cursor = conn.cursor()

    def save_all_data(self, data):
        if(len(data['genre'])>0):
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

        if(len(data['person'])>0):
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

        if(len(data['film_work'])>0):
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

        if(len(data['genre_film_work'])>0):
            args = ','.join(self.cursor.mogrify("(%s, %s, %s, %s)", item).decode() for item in data['genre_film_work'])
            self.cursor.execute(f"""
            INSERT INTO content.genre_film_work
            (id, film_work_id, genre_id, created_at)
            VALUES {args}
            ON CONFLICT (id) DO UPDATE SET  film_work_id=EXCLUDED.film_work_id,
                                            genre_id=EXCLUDED.genre_id,
                                            created_at=EXCLUDED.created_at

            """)

        if(len(data['person_film_work'])>0):
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