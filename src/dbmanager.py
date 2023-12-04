import psycopg2


class PostgreSQL:
    CONN = psycopg2.connect(
        host="localhost",
        database="vacancies",
        user="postgres",
        password="123456")

    CUR = CONN.cursor()

    @classmethod
    def commit_table(cls):
        cls.CONN.commit()

    @classmethod
    def create_tables(cls):
        cls.CUR.execute("CREATE TABLE employees"
                        "(employer_id int PRIMARY KEY,"
                        "name varchar(50) NOT NULL,"
                        "description text,"
                        "area varchar(20),"
                        "open_vacancies int);")

        cls.CUR.execute("CREATE TABLE vacancies"
                        "(vacancy_id int PRIMARY KEY,"
                        "employer_id int REFERENCES employees(employer_id),"
                        "title text,"
                        "salary_from int,"
                        "salary_to int,"
                        "requirement text,"
                        "responsibility text,"
                        "url text);")

    @classmethod
    def full_table_e(cls, employer_id, name, description, area, open_vacancies):
        cls.CUR.execute("INSERT INTO employees VALUES (%s, %s, %s, %s, %s)",
                        (employer_id, name, description, area, open_vacancies))

    @classmethod
    def full_table_v(cls, vacancy_id, employer_id, name, salary_from, salary_to, requirement, responsibility, url):
        cls.CUR.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (vacancy_id, employer_id, name, salary_from, salary_to, requirement, responsibility, url))

    @classmethod
    def drop_tables(cls):
        cls.CUR.execute("DROP TABLE IF EXISTS employees CASCADE;"
                        "DROP TABLE IF EXISTS vacancies")


class DBManager:
    CONN = psycopg2.connect(
        host="localhost",
        database="vacancies",
        user="postgres",
        password="123456")

    CUR = CONN.cursor()

    @classmethod
    def get_companies_and_vacancies_count(cls):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        cls.CUR.execute("SELECT name, open_vacancies FROM employees "
                        "ORDER BY name")
        rows = cls.CUR.fetchall()
        for row in rows:
            print(row)

    @classmethod
    def get_all_vacancies(cls):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        """
        cls.CUR.execute("SELECT name, title, salary_from, salary_to, url FROM employees, vacancies "
                        "ORDER BY name")
        rows = cls.CUR.fetchall()
        for row in rows:
            print(row)

    @classmethod
    def get_avg_salary(cls):
        """
        Получает среднюю зарплату по вакансиям
        """
        cls.CUR.execute("SELECT AVG (salary_from) as avg_salary FROM vacancies")
        rows = cls.CUR.fetchall()
        for row in rows:
            print(row)

    @classmethod
    def get_vacancies_with_higher_salary(cls):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        cls.CUR.execute("SELECT name, title, salary_from, salary_to, url FROM vacancies, employees "
                        "WHERE salary_from > (SELECT AVG (salary_from) FROM vacancies)"
                        "ORDER BY salary_from")
        rows = cls.CUR.fetchall()
        for row in rows:
            print(row)

    @classmethod
    def get_vacancies_with_keyword(cls, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        """
        cls.CUR.execute("SELECT name, title, salary_from, salary_to, url FROM vacancies, employees "
                        f"WHERE title LIKE '%{keyword}%'")
        rows = cls.CUR.fetchall()
        for row in rows:
            print(row)
