import asyncio
import json
from typing import List

import aiohttp

from utilities import Job

API_URL = "https://api.superjob.ru/2.0/"
CITY_ID = 4
API_TOKEN = "v3.r.136524780.93d3bb566c061d4ae702d6795605d847ba8ec7f9.9ce2a85e833475b168303ff081efabb9d06ee645"


class SuperJob:
    def __init__(self, api_token: str, client: aiohttp.ClientSession):
        self.client = client
        self.headers = {
            "X-Api-App-Id": api_token,
            "Content-Type": "application/x-www-form-urlencoded"
        }

    async def get_vacancies(self, count: int, town_id: int = CITY_ID) -> List[Job]:
        async with self.client.get(
                API_URL + "vacancies",
                headers=self.headers,
                params={"town": town_id, "count": count}
        ) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            vacancies = (await response.json())["objects"]

            result = []

            for vacancy in vacancies:
                result.append(Job(
                    title=vacancy["profession"],
                    salary_from=vacancy["payment_from"],
                    salary_to=vacancy["payment_to"],
                    currency=vacancy["currency"],
                    description=" ".join(vacancy["candidat"].replace("\n", " ").split()),
                    url=vacancy["link"]
                ))

            return result