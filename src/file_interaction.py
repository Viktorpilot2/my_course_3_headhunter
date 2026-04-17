import psycopg2
from psycopg2.extensions import connection


def create_database(new_database: str, params: dict) -> None:
    """Создание новой БД"""
    try:
        conn = psycopg2.connect(database="postgres", **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS {new_database};")
            cur.execute(f"CREATE DATABASE {new_database};")
    except psycopg2.DatabaseError as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        conn = None
    if conn is not None:
        conn.close()


def create_table(conn: connection) -> None:
    """Создание таблиц БД"""
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS company(
                    company_id INT PRIMARY KEY,
                    company_name VARCHAR(100),
                    company_url VARCHAR(100),
                    count_vacancy INT)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS vacancy(
                    vacancy_id SERIAL PRIMARY KEY,
                    vacancy VARCHAR(100),
                    vacancy_url VARCHAR(100),
                    salary_from INT,
                    salary_to INT,
                    area VARCHAR(100),
                    published_date DATE,
                    company_id INT REFERENCES company(company_id))""")
        conn.commit()


def insert_table(list_data_employers: list[dict], list_data_vacancy: list[dict], conn: connection) -> None:
    """Заполнение таблиц, данными по работодателям и вакансиям"""
    with conn.cursor() as cur:
        for i in list_data_employers:
            cur.execute(
                "INSERT INTO company(company_id, company_name, company_url, count_vacancy) VALUES (%s, %s, %s, %s)",
                tuple(i.values()),
            )
        for i in list_data_vacancy:
            cur.execute(
                """INSERT INTO vacancy(vacancy, vacancy_url, salary_from, salary_to, area, published_date, company_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                tuple(i.values()),
            )
        conn.commit()
