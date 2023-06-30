import json
import os
from abc import ABC, abstractmethod

import json

import requests

API_KEY_SJ: str = "v3.r.137641108.6cde3c0a45d757a8dda83c208eac505a7e929aee.1ffce3b1beb8d72068c1117e275f2b36d532d224"
VACANCIES: int = 3
PER_PAGES: int = 2
API_URL_HH = "https://api.hh.ru/vacancies"
EUR: float = 90.5
USD: float = 85.3


class AbstractClassApi(ABC):
    """
    Абстрактный класс для создания классов по работе с API

    """

    @abstractmethod
    def get_request(self):
        """
        Метод для получения запроса от API
        """
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HHApi(AbstractClassApi):
    """
     Класс для работы по API c сайтом www.hh.ru

    """

    # api_url = "https://api.hh.ru/vacancies"

    def get_request(self, k_word, pages=10, api_url=API_URL_HH):
        """
        Метод класса HHApi, который делает запрос на сайт hh.ru  по API (результат в JSON формате)

        """
        params = {'text': k_word, 'page': pages, 'per_page': PER_PAGES}

        try:
            return requests.get(api_url, params=params).json()['items']
        except requests.exceptions.ConnectionError as errors:
            print(f'ATTENTION!!!!! ***connection error during request*** \n {errors}\n')

    def get_vacancies(self, k_word):
        """
        Метод получения списка вакансий по ключевому слову

        """

        list_vacancies = []
        for item in range(PER_PAGES):
            data = self.get_request(k_word, item)
            list_vacancies.append(data)
        return list_vacancies


class SJApi(AbstractClassApi):
    """
    Класс для работы по API c сайтом www.superjob.ru

    """

    def get_request(self, k_word, pages):
        authorization = {'X-Api-App-Id': API_KEY_SJ}
        params = {'keyword': k_word, 'page': pages, 'count': VACANCIES}

        try:
            return requests.get('https://api.superjob.ru/2.0/vacancies/', headers=authorization, params=params).json()[
                "objects"]
        except requests.exceptions.ConnectionError as errors:
            print(f'ATTENTION!!!!! ***connection error during request*** \n {errors}\n')

    def get_vacancies(self, k_word='Python developer'):
        """
        Метод получения списка вакансий по ключевому слову

        """

        list_vacancies = []
        for item in range(PER_PAGES):
            data = self.get_request(k_word, item)
            list_vacancies.append(data)
        return list_vacancies


class Vacancy:
    """
    Клас вакансии

    """

    def __init__(self, title, salary_from, salary_to, salary_currency, url, employer_name, address):
        self.__title = title
        self.__url = url
        self.__employer_name = employer_name
        self.__address = address
        self.__salary_from = salary_from
        self.__salary_to = salary_to
        self.__salary_currency = salary_currency

    def __str__(self):
        if self.__salary_currency:
            self.__salary_currency = f"Вилка заработной платы({self.__salary_currency}) "
        else:
            self.__salary_currency = "Уровень заработной платы не указан"
        if self.__salary_from:
            self.__salary_from = self.__salary_from
        else:
            self.__salary_from = " нет данных "
        if self.__salary_to:
            self.__salary_to = self.__salary_to
        else:
            self.__salary_to = " нет данных "
        if not self.__address:
            self.__address = "Адрес не указан"

        rez = f"Компания работодатель: {self.__employer_name}  / Вакансия:  {self.__title}\n" \
              f"Ссылка на страницу вакансии: {self.__url} \n" \
              f"{self.__salary_currency} от: {self.__salary_from} до: {self.__salary_to}\n" \
              f"Адрес работодателя: {self.__address}"
        return rez

    def __gt__(self, other):

        """
        Метод сравнения по минимальной зарплате

        """
        if not other.__salary_from:
            return True
        if not self.__salary_from:
            return False
        return self.__salary_from >= other.__salary_from


class AbstractClassJCONSaver(ABC):
    """
    Абстрактный класс для классов, по обработке данных о вакансиях

    """

    @abstractmethod
    def add_vacancy(self):
        pass

    @abstractmethod
    def select(self):
        pass


class JSONSaver(AbstractClassJCONSaver):
    """
    Класс обработки данных вакансий
    """

    def __init__(self, key_word: str, name_file: str):
        self.__file_name = f"{key_word.lower()}_{name_file.lower()}.json"

    @property
    def filename(self):
        return self.__file_name

    def add_vacancy(self, data):
        """Добавляет вакансии в файл 'self.__file_name'"""
        with open(self.__file_name, 'w', encoding="UTF-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def select(self):
        """Создаем экземпляры с нужными атрибутами. Переводим, если нужно, в рубли """

        list_vac = []
        salary_from = None
        salary_to = None
        salary_currency = None

        with open(self.__file_name, "r", encoding="UTF-8") as f:
            data = json.load(f)

        if "hh" in self.filename:
            for row in data:
                if row["salary"] and row["salary"]["to"] and row["salary"]["from"]:
                    salary_from, salary_to, salary_currency = row["salary"]["from"], row["salary"]["to"], row["salary"][
                        "currency"]
                    if row["salary"]["currency"].upper() == "EUR":
                        salary_from = row["salary"]["from"] *EUR
                        salary_to = row["salary"]["to"] * EUR
                    if row["salary"]["currency"].upper() == "USD":
                        salary_from = row["salary"]["from"] * USD
                        salary_to = row["salary"]["to"] * USD
                    salary_currency = "RUB"

                list_vac.append(Vacancy(
                    row["name"],
                    salary_from,
                    salary_to,
                    salary_currency,
                    row["alternate_url"],
                    row["employer"]["name"],
                    row["area"]["name"]))

        if "sj" in self.filename:
            for row in data:
                if row["currency"]:
                    salary_from, salary_to, salary_currency = row["payment_from"], row["payment_to"], row["currency"]

                    if row["currency"].upper() == "EUR":
                        salary_from = row["payment_from"] * EUR
                        salary_to = row["payment_to"] * EUR
                    if row["currency"].upper == "USD":
                        salary_from = row["payment_from"] * USD
                        salary_to = row["payment_to"] * USD
                    salary_currency = "RUB"

                list_vac.append(Vacancy(
                    row["profession"],
                    salary_from,
                    salary_to,
                    salary_currency,
                    row["link"],
                    row["firm_name"],
                    row["address"]))

        return list_vac
