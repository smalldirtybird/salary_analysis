import requests
import os
from itertools import count
from dotenv import load_dotenv
from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif not salary_from:
        return salary_to * 0.8
    elif not salary_to:
        return salary_from * 1.2
    else:
        return None


def predict_rub_salary_for_hh(vacancy):
    salary = vacancy['salary']
    if salary and salary['currency'] == 'RUR':
        return predict_salary(salary['from'], salary['to'])


def get_job_statistics_from_hh(email, profession, language):
    host = 'https://api.hh.ru/'
    path = 'vacancies'
    url = os.path.join(host, path)
    headers = {'User-Agent': email}
    search_fields = 'в названии вакансии'
    area_id = 1
    vacancy_age_in_days = 30
    quantity_of_vacancies_on_page = 100
    vacancies = []
    for page in count():
        parameters = {'text': f'{profession} {language}',
                      'vacancy_search_fields': search_fields,
                      'area': area_id,
                      'period': vacancy_age_in_days,
                      'per_page': quantity_of_vacancies_on_page,
                      'page': page
                      }
        page_response = requests.get(url,
                                     headers=headers,
                                     params=parameters)
        page_response.raise_for_status()
        page_content = page_response.json()
        for vacancy in page_content['items']:
            vacancies.append(vacancy)
        max_page = 19
        if page == page_content['pages'] or page == max_page:
            break
    salaries = []
    for vacancy in vacancies:
        average_salary = predict_rub_salary_for_hh(vacancy)
        if average_salary:
            salaries.append(average_salary)
    return {
        'vacancies_found': page_content['found'],
        'vacancies_processed': len(salaries),
        'average_salary': int(sum(salaries) / len(salaries))
    }


def predict_rub_salary_for_sj(vacancy):
    if vacancy['currency'] == 'rub':
        return predict_salary(vacancy['payment_from'], vacancy['payment_to'])


def get_job_statistics_from_sj(token, profession, language):
    host = 'https://api.superjob.ru/2.0/'
    path = 'vacancies'
    url = os.path.join(host, path)
    headers = {'X-Api-App-Id': token}
    town_id = 4
    profession_identifiers = [48]
    quantity_of_vacancies_on_page = 100
    vacancies = []
    for page in count():
        parameters = {'town': town_id,
                      'catalogues': profession_identifiers,
                      'keywords': [profession, language],
                      'page': page,
                      'count': quantity_of_vacancies_on_page
                      }
        page_response = requests.get(url,
                                     headers=headers,
                                     params=parameters)
        page_response.raise_for_status()
        page_content = page_response.json()
        for vacancy in page_content['objects']:
            vacancies.append(vacancy)
        if not page_content['more']:
            break
    salaries = []
    for vacancy in vacancies:
        average_salary = predict_rub_salary_for_sj(vacancy)
        if average_salary:
            salaries.append(average_salary)
    return {
        'vacancies_found': len(vacancies),
        'vacancies_processed': len(salaries),
        'average_salary': int(sum(salaries) / len(salaries))
        }


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
    profession_name = 'программист'
    user_email = os.environ['EMAIL']
    sj_token = os.environ['SJ_TOKEN']
    programming_languages = ['TypeScript', 'Swift', 'Scala',
                             'Objective-C', 'Shell', 'Go',
                             'C', 'C#', 'C++', 'PHP', 'Ruby',
                             'Python', 'Java', 'JavaScript'
                             ]
    job_statistics_from_hh = {}
    job_statistics_from_sj = {}
    for programming_language in programming_languages:
        job_statistics_from_hh[programming_language] = get_job_statistics_from_hh(
            user_email, profession_name, programming_language)
        job_statistics_from_sj[programming_language] = get_job_statistics_from_sj(
            sj_token, profession_name, programming_language)
    create_table_with_statistics(job_statistics_from_hh, 'HeadHunter Moscow')
    create_table_with_statistics(job_statistics_from_sj, 'SuperJob Moscow')
