import os

import psycopg2
from dotenv import load_dotenv

from src.api_interaction import get_api_data_employers, get_api_data_vacancy
from src.file_interaction import create_database, create_table, insert_table
from src.vacancy_interaction import DBManager

load_dotenv()
params = {
    "host": os.getenv("HOST"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("PORT"),
}


def main(list_employers: list[str], new_database: str, word: str) -> None:
    """Функция, объединяющая функциональность всего проекта"""
    list_data_employers = get_api_data_employers(list_employers)
    list_data_vacancy = get_api_data_vacancy(list_data_employers)
    create_database(new_database, params)
    try:
        conn = psycopg2.connect(database=new_database, **params)
        create_table(conn)
        insert_table(list_data_employers, list_data_vacancy, conn)
        example_1 = DBManager(conn)
        if list_data_employers:
            print("Список названий компаний и количества вакансий в них: ")
            [print(f"   {i}") for i in example_1.get_companies_and_vacancies_count()]
            print("Список всех вакансий: ")
            [print(f"   {i}") for i in example_1.get_all_vacancies()]
            print(example_1.get_avg_salary())
            print("Список всех вакансий, у которых зарплата выше средней по всем вакансиям: ")
            [print(f"   {i}") for i in example_1.get_vacancies_with_higher_salary()]
            print(f"Список всех вакансий, в названии которых содержится слово '{word}': ")
            [print(f"   {i}") for i in example_1.get_vacancies_with_keyword(word)]
        else:
            print("Не найдено ни одной компании с заданными названиями.")
    except psycopg2.DatabaseError as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        conn = None
    if conn is not None:
        conn.close()


if __name__ == "__main__":
    list_employers_ = [
        "Авиакомпания Победа",
        "Уральские авиалинии, Авиакомпания",
        "ЧПОУ Авиашкола Аэрофлота",
        "Азур Эйр",
        "Хабаровские авиалинии",
        'Акционерное общество "Энергоспецмонтаж"',
        "Банк ВТБ (ПАО)",
        "СИБУР, Группа компаний",
        "X5 Tech",
        "Группа ЛСР",
    ]
    main(list_employers_, new_database="my_db", word="руководитель")
