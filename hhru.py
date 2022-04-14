import json
import os
from datetime import time

import aiohttp

class HHRU:
    def __init__(self):
        self.count = 0

    async def getPage(self, job, page):
        params = {
            'text': 'NAME:' + job,  # Текст фильтра. В имени должно быть слово "Аналитик"
            'area': 1,  # Поиск ощуществляется по вакансиям города Москва
            'page': page,  # Индекс страницы поиска на HH
            'per_page': 1  # Кол-во вакансий на 1 странице
        }

        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.hh.ru/vacancies', params=params) as req:
                return await req.json()

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
        url = response["items"][0]["alternate_url"]
        return url


# hhru = HHRU()
# for i in range(2):
#     response = await hhru.getPage()
#     print(response)
#     print("Название:", hhru.parse_name(response))
#     print("Зарплата:", hhru.parse_salary(response))
#     print("требования:", hhru.parse_requirements(response))
#     print("Обязанности:", hhru.parse_responsibilities(response))
#     print("URL: ", hhru.parse_url(response))
