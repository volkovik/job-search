import json
import os
from datetime import time
from utilities import Job

import requests


class HHRU:
    def __init__(self, name):
        self.name = name
        self.count = 0

    def getById(self, id):
        """
                Создаем метод для получения страницы со списком вакансий.
                Аргументы:
                    page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
                """
        # Справочник для параметров GET-запроса

        req = requests.get('https://api.hh.ru/vacancies/' + str(id))  # Посылаем запрос к API
        data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        return json.loads(data)

    def getPage(self, page=None):
        """
        Создаем метод для получения страницы со списком вакансий.
        Аргументы:
            page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
        """
        if page is None:
            page = self.count
            self.count += 1
        # Справочник для параметров GET-запроса
        params = {
            'text': 'NAME:' + self.name,  # Текст фильтра. В имени должно быть слово "Аналитик"
            'area': 1,  # Поиск ощуществляется по вакансиям города Москва
            'page': page,  # Индекс страницы поиска на HH
            'per_page': 1  # Кол-во вакансий на 1 странице
        }

        req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
        data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        return json.loads(data)

    # def parse_job(self, response): todo
    #     return Job(url: str
    # title: str
    # salary_from: int
    # salary_to: int
    # currency: str
    # description: str)

    def parse_name(self, response):
        return response["items"][0]["name"]

    def parse_salary(self, response):
        salary = response["items"][0]["salary"]
        if salary["to"] is None:
            return "от " + str(salary["from"]) + ". валюта: " + str(salary["currency"])
        elif salary["from"] is None:
            return "Обговаривается отдельно"
        else:
            return "от " + str(salary["from"]) + " до " + str(salary["to"]) + ". валюта: " + salary[
                "currency"]

    def parse_requirements(self, response):
        snippet = response["items"][0]["snippet"]
        return snippet["requirement"]

    def parse_responsibilities(self, response):
        snippet = response["items"][0]["snippet"]
        return snippet["responsibility"]

    def parse_url(self, response):
        url = response["items"][0]["url"]
        return url


# hhru = HHRU("Программист")
# for i in range(2):
#     response = hhru.getPage()
#     print(response)
#     # print(json.dump(response, open("name.json", mode="w"), ensure_ascii=False))
#     print("Название:", hhru.parse_name(response))
#     print("Зарплата:", hhru.parse_salary(response))
#     print("требования:", hhru.parse_requirements(response))
#     print("Обязанности:", hhru.parse_responsibilities(response))
#     print("URL: ", hhru.parse_url(response))

hhru = HHRU("Программист")
print(hhru.getById(7760476))

# for page in range(0, 1):
#
#     # Преобразуем текст ответа запроса в справочник Python
#     jsObj = json.loads(HHRU.getPage(page))
#
#     # Сохраняем файлы в папку {путь до текущего документа со скриптом}\docs\pagination
#     # Определяем количество файлов в папке для сохранения документа с ответом запроса
#     # Полученное значение используем для формирования имени документа
#     nextFileName = './docs/pagination/{}.json'.format(len(os.listdir('./docs/pagination')))
#
#     # Создаем новый документ, записываем в него ответ запроса, после закрываем
#     f = open(nextFileName, mode='w', encoding='utf8')
#     f.write(json.dumps(jsObj, ensure_ascii=False))
#     f.close()
#
#     # Проверка на последнюю страницу, если вакансий меньше 2000
#     if (jsObj['pages'] - page) <= 1:
#         break
#
#     # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
#     time.sleep(0.25)
