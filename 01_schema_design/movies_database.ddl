CREATE SCHEMA IF NOT EXISTS content;

DROP TABLE IF EXISTS content.film_work;
DROP TABLE IF EXISTS content.person_film_work;
DROP TABLE IF EXISTS content.person;
DROP TABLE IF EXISTS content.genre_film_work;
DROP TABLE IF EXISTS content.genre;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    person_id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    role varchar(128) NOT NULL,
    created timestamp with time zone
);

CREATE INDEX person_film_work_person_id ON content.person_film_work(person_id);
CREATE INDEX person_film_work_film_work_id ON content.person_film_work(film_work_id);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name varchar(128) NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    created timestamp with time zone
);

CREATE INDEX genre_film_work_genre_id ON content.genre_film_work(genre_id);
CREATE INDEX genre_film_work_film_work_id ON content.genre_film_work(film_work_id);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name varchar(32) NOT NULL,
    description text NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);