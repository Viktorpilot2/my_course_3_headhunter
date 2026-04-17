import requests


def get_api_data_employers(list_employers: list[str]) -> list[dict]:
    """Получение данных о работодателях через API"""
    url = "https://api.hh.ru/employers"
    list_data_employers = []
    for employer in list_employers:
        params = {"text": employer}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            for i in response.json().get("items", {}):
                company_id = i.get("id", None)
                vacancy_url = i.get("vacancies_url", None)
                count_vacancy = i.get("open_vacancies", None)
                dict_company = {
                    "company_id": company_id,
                    "company_name": employer,
                    "vacancy_url": vacancy_url,
                    "count_vacancy": count_vacancy,
                }
                list_data_employers.append(dict_company)
        else:
            print(f"Ошибка при получении данных о работодателе {employer}: {response.status_code}")
            continue
    return list_data_employers


def get_api_data_vacancy(list_data_employers: list[dict]) -> list[dict]:
    """Получение данных о вакансиях работодателей, полученных через API"""
    list_data_vacancy = []
    for employer in list_data_employers:
        if employer.get("vacancy_url") is not None:
            response = requests.get(employer.get("vacancy_url"))
            if response.status_code == 200:
                for i in response.json().get("items", {}):
                    data = {
                        "vacancy": i.get("name", None),
                        "vacancy_url": i.get("area", {}).get("url", None) if i.get("area") is not None else None,
                        "salary_from": i.get("salary", {}).get("from", None) if i.get("salary") is not None else None,
                        "salary_to": i.get("salary", {}).get("to", None) if i.get("to") is not None else None,
                        "area": i.get("area", {}).get("name", None) if i.get("area") is not None else None,
                        "published_date": i.get("published_at", None),
                        "company_id": employer.get("company_id"),
                    }
                    list_data_vacancy.append(data)
            else:
                print(f"Ошибка при получении данных о вакансиях работодателя {employer[0]}: {response.status_code}")
                continue
        else:
            continue
    return list_data_vacancy


if __name__ == "__main__":
    list_employers_ = [
        "Авиакомпания Победа",
        "Уральские авиалинии, Авиакомпания",
    ]
    list_data_employers_ = get_api_data_employers(list_employers_)
    print(list_data_employers_)
    print(get_api_data_vacancy(list_data_employers_))
