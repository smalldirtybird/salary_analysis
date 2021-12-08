import requests
import os
import collections
from itertools import count
from pprint import pprint


def predict_rub_salary(vacancy):
    salary = vacancy['salary']
    if salary['currency'] != 'RUR':
        return None
    elif salary['from'] and salary['to']:
        return (salary['from'] + salary['to']) / 2
    elif not salary['from']:
        return salary['to'] * 0.8
    else:
        return salary['from'] * 1.2


def get_vacancies_with_salaries(parameters):
    host = 'https://api.hh.ru/'
    method = 'vacancies'
    url = os.path.join(host, method)
    headers = {'User-Agent': 'smalldirtybird@gmail.com'}
    vacancies = []
    for page in count():
        parameters['page'] = page
        page_response = requests.get(url,
                                     headers=headers,
                                     params=parameters)
        page_response.raise_for_status()
        page_content = page_response.json()
        if page >= page_content['pages']:
            break
        for item in page_content['items']:
            vacancies.append(item)
    salaries = []
    for vacancy in vacancies:
        salary = predict_rub_salary(vacancy)
        if salary:
            salaries.append(salary)
    if len(vacancies):
        vacancies_with_salaries = {
            'vacancies_found': len(vacancies),
            'vacancies_processed': len(salaries),
            'average_salary': int(sum(salaries) / len(salaries))
            }
        return vacancies_with_salaries


if __name__ == '__main__':
    profession = 'программист'
    programming_languages = ['TypeScript', 'Swift', 'Scala', 'Objective-C', 'Shell',
        'Go', 'C', 'C#', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']
    vacancies_by_languages = collections.defaultdict(int)
    for language in programming_languages:
        vacancy_settings = {'text': f'{profession} {language}',
                            'vacancy_search_fields': 'в названии вакансии',
                            'area': '1',
                            'period': 30,
                            'per_page': 100,
                            'only_with_salary': True
                            }
        vacancies_by_languages[language] = get_vacancies_with_salaries(vacancy_settings)
    pprint(vacancies_by_languages)
