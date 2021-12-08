import requests
import os
import collections
from itertools import count
from dotenv import load_dotenv
from terminaltables import AsciiTable
from pprint import pprint


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif not salary_from:
        return salary_to * 0.8
    else:
        return salary_from * 1.2


def predict_rub_salary_for_hh(vacancy):
    salary = vacancy['salary']
    if salary['currency'] != 'RUR':
        return None
    else:
        return predict_salary(salary['from'], salary['to'])


def get_vacancies_from_hh(profession_name, languages):
    host = 'https://api.hh.ru/'
    method = 'vacancies'
    url = os.path.join(host, method)
    headers = {'User-Agent': 'smalldirtybird@gmail.com'}
    hh_job_statistics = collections.defaultdict(dict)
    for language in languages:
        vacancies = []
        for page in count():
            parameters = {'text': f'{profession_name} {language}',
                          'vacancy_search_fields': 'в названии вакансии',
                          'area': '1',
                          'period': 30,
                          'per_page': 100,
                          'only_with_salary': True,
                          'page': page
                          }
            page_response = requests.get(url,
                                         headers=headers,
                                         params=parameters)
            page_response.raise_for_status()
            page_content = page_response.json()
            if page >= page_content['pages']:
                break
            for vacancy in page_content['items']:
                vacancies.append(vacancy)
        salaries = []
        for vacancy in vacancies:
            salary = predict_rub_salary_for_hh(vacancy)
            if salary:
                salaries.append(salary)
        if len(vacancies):
            hh_job_statistics[language] = {
                'vacancies_found': len(vacancies),
                'vacancies_processed': len(salaries),
                'average_salary': int(sum(salaries) / len(salaries))
            }
            print(hh_job_statistics[language])
    create_table_with_statistics(hh_job_statistics, 'HeadHunter Moscow')


def predict_rub_salary_for_sj(vacancy):
    if vacancy['currency'] != 'rub':
        return None
    else:
        return predict_salary(vacancy['payment_from'], vacancy['payment_to'])


def get_vacancy_from_sj(token, profession_name, languages):
    host = 'https://api.superjob.ru/2.0/'
    method = 'vacancies'
    url = os.path.join(host, method)
    headers = {'X-Api-App-Id': token}
    sj_job_statistics = collections.defaultdict(dict)
    for language in languages:
        vacancies = []
        for page in count():
            parameters = {'town': '4',
                          'catalogues': [48],
                          'keywords': [profession_name, language],
                          'no_agreement': 1,
                          'page': page,
                          'count': 100
                          }
            page_response = requests.get(url, headers=headers, params=parameters)
            page_response.raise_for_status()
            page_content = page_response.json()
            for vacancy in page_content['objects']:
                vacancies.append(vacancy)
            if not page_content['more']:
                break
        salaries = []
        for vacancy in vacancies:
            salary = predict_rub_salary_for_sj(vacancy)
            if salary:
                salaries.append(salary)
        if len(vacancies):
            sj_job_statistics[language] = {
                'vacancies_found': len(vacancies),
                'vacancies_processed': len(salaries),
                'average_salary': int(sum(salaries) / len(salaries))
            }
    create_table_with_statistics(sj_job_statistics, 'SuperJob Moscow')


def create_table_with_statistics(vacancy_statistics, table_name):
    title = table_name
    table_headers = ['Язык программирования',
                     'Вакансий найдено',
                     'Вакансий обработано',
                     'Средняя зарплата']
    table_rows = [table_headers]
    for statistic in vacancy_statistics:
        table_row = [statistic,
                     vacancy_statistics[statistic]['vacancies_found'],
                     vacancy_statistics[statistic]['vacancies_processed'],
                     vacancy_statistics[statistic]['average_salary']]
        table_rows.append(table_row)
    table_instance = AsciiTable(table_rows, title)
    print(table_instance.table)


if __name__ == '__main__':
    load_dotenv()
    profession = 'программист'
    sj_token = os.environ['SJ_TOKEN']
    programming_languages = ['TypeScript', 'Swift', 'Scala', 'Objective-C', 'Shell',
                             'Go', 'C', 'C#', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']
    get_vacancies_from_hh(profession, programming_languages)
    get_vacancy_from_sj(sj_token, profession, programming_languages)
