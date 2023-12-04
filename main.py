from src.hh_requests import *
from src.dbmanager import *


def main():
    employers_id = [3529, 78638, 4023, 1740, 4352, 2748, 23427, 87021, 2180, 17796]

    PostgreSQL.drop_tables()
    PostgreSQL.create_tables()

    employers = []
    for employer_id in employers_id:
        employers.append(Employer.create_employer(employer_id))

    for employer in employers:
        PostgreSQL.full_table_e(employer.id, employer.name, employer.description, employer.area, employer.open_vacancies)
        headers = {'User-Agent': 'admin'}
        parameters_vacancies = {'employer_id': employer.id, 'per_page': 100}
        vacancies = requests.get(url_vacancies, headers=headers, params=parameters_vacancies).json()
        for vacancy in vacancies['items']:
            v = Vacancy.create_vacancy(vacancy)
            url = f"https://hh.ru/vacancy/{v.url}"
            PostgreSQL.full_table_v(v.url, employer.id, v.name, v.salary_from, v.salary_to, v.requirement, v.responsibility,
                                    url)

    PostgreSQL.commit_table()

    print("База данных работодателей и вакансий сформирована.")
    while True:
        command = input("""
1 - Получить список всех компаний и количество вакансий у каждой компании;
2 - Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию;
3 - Получить среднюю зарплату по вакансиям;
4 - Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям;
5 - Получить список всех вакансий по ключевому слову;
6 - Закрыть программу.
Введите команду: """)
        if command not in '123456':
            print("Команда должна быть цифрой от 1 до 6")
            continue

        if command == '1':
            DBManager.get_companies_and_vacancies_count()
        elif command == '2':
            DBManager.get_all_vacancies()
        elif command == '3':
            DBManager.get_avg_salary()
        elif command == '4':
            DBManager.get_vacancies_with_higher_salary()
        elif command == '5':
            keyword = input("Введите ключевое слово: ")
            DBManager.get_vacancies_with_keyword(keyword)
        elif command == '6':
            break


if __name__ == '__main__':
    main()
