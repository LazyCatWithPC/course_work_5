import requests

url_employees = 'https://api.hh.ru/employers/'
url_vacancies = 'https://api.hh.ru/vacancies/'


class Employer:
    def __init__(self, id, name, description, area, open_vacancies):
        self.id = id
        self.name = name
        self.description = description
        self.area = area
        self.open_vacancies = open_vacancies

    def __repr__(self):
        return f"""{self.name}
{self.description}
Город: {self.area}
Количество вакансий: {self.open_vacancies}"""

    @staticmethod
    def create_employer(employer_id: int):
        headers = {'User-Agent': 'admin'}
        parameters = {'employer_id': employer_id}

        response = requests.get(url_employees + str(employer_id), headers=headers, params=parameters).json()

        bad_words = ['</strong>', '<strong>', '<p>', '</p>', '&laquo;', '&raquo;', '&nbsp;', '<em>', '</em>', '<br />',
                     '</li>', '<li>', '&quot;', '<ul>', '</ul>']

        name = response['name']
        open_vacancies = response['open_vacancies']
        area = response['area']['name']
        description = response['description']
        for word in bad_words:
            if word in description:
                description = description.replace(word, '')

        return Employer(employer_id, name, description, area, open_vacancies)


class Vacancy:

    def __init__(self, url, name, salary_from, salary_to, requirement, responsibility):
        self.url = url
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.requirement = requirement
        self.responsibility = responsibility

    def __repr__(self):
        return f"""{self.name}
    {self.url}
    {self.salary_from} - {self.salary_to}
    {self.requirement}
    {self.responsibility}"""

    @staticmethod
    def create_vacancy(data):
        vacancy_id = data['id']
        name = data['name']
        if data['salary'] is not None:
            salary_from = data['salary'].get('from', 0)
            salary_to = data['salary'].get('to', 0)
        else:
            salary_from = None
            salary_to = None

        requirement = data['snippet']['requirement']
        responsibility = data['snippet']['responsibility']

        return Vacancy(vacancy_id, name, salary_from, salary_to, requirement, responsibility)
