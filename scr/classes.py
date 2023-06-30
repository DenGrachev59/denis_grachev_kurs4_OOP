from abc import ABC, abstractmethod
import json
import requests

""" Постоянные переменные """
API_KEY_SJ: str = "v3.r.137641108.6cde3c0a45d757a8dda83c208eac505a7e929aee.1ffce3b1beb8d72068c1117e275f2b36d532d224"
VACANCIES: int = 200
PER_PAGES: int = 10
API_URL_HH = "https://api.hh.ru/vacancies"
API_URL_SJ ="https://api.superjob.ru/2.0/vacancies/"
EUR = 90
USD = 85


class AbstractClassApi(ABC):
    """
    Абстрактный класс для создания классов по работе с API
    """

    @abstractmethod
    def get_request(self):
        """
        Получение запроса от API
        """
        pass

    @abstractmethod
    def get_vacancies(self):
        """
        Получение вакансий
        """
        pass


class HHApi(AbstractClassApi):
    """
     Класс для работы по API c сайтом www.hh.ru
    """

    def get_request(self, k_word, pages=10, api_url=API_URL_HH):
        """
        Метод класса HHApi, который делает запрос на сайт hh.ru по API (результат в JSON формате)
        """
        params = {'text': k_word, 'page': pages, 'per_page': PER_PAGES}

        try:
            return requests.get(api_url, params=params).json()['items']
        except requests.exceptions.ConnectionError as errors:
            print(f'ATTENTION!!!!! ***connection error during request*** \n {errors}\n')

    def get_vacancies(self, k_word):

        list_vacancies = []
        for item in range(PER_PAGES):
            data = self.get_request(k_word, item)
            list_vacancies.extend(data)
        return list_vacancies


class SJApi(AbstractClassApi):
    """
    Класс для работы по API c сайтом superjob.ru
    """

    def get_request(self, k_word, pages, api_url=API_URL_SJ):
        authorization = {'X-Api-App-Id': API_KEY_SJ}
        params = {'keyword': k_word, 'page': pages, 'count': VACANCIES}

        try:
            return requests.get(api_url, headers=authorization, params=params).json()[
                "objects"]
        except requests.exceptions.ConnectionError as errors:
            print(f'ATTENTION!!!!! ***connection error during request*** \n {errors}\n')

    def get_vacancies(self, k_word='Python developer'):

        list_vacancies = []
        for item in range(PER_PAGES):
            data = self.get_request(k_word, item)
            list_vacancies.extend(data)
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
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency

    def __str__(self):
        if self.salary_currency:
            self.salary_currency = f"Вилка заработной платы ({self.salary_currency}) "
        else:
            self.salary_currency = "Уровень заработной платы не указан"
        if self.salary_from:
            self.salary_from = self.salary_from
        else:
            self.salary_from = ""
        if self.salary_to:
            self.salary_to = self.salary_to
        else:
            self.salary_to = ""
        if not self.__address:
            self.__address = "Адрес не указан"

        rez = f"  Компания работодатель: {self.__employer_name} \n  Вакансия:  {self.__title}\n" \
              f"  Ссылка на страницу вакансии: {self.__url} \n" \
              f"  {self.salary_currency} от: {self.salary_from} до: {self.salary_to}\n" \
              f"  Адрес работодателя: {self.__address}"
        return rez

    def __gt__(self, other):
        """
        Метод сравнения по минимальной зарплате
        """

        if not other.salary_from:
            return True
        if not self.salary_from:
            return False
        return self.salary_from >= other.salary_from


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
        with open(self.__file_name, 'w', encoding="UTF-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

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
                    salary_from = row["salary"]["from"]
                    salary_to = row["salary"]["to"]
                    salary_currency = row["salary"]["currency"]

                    if row["salary"]["currency"].upper() == "EUR":
                        salary_from = row["salary"]["from"] * EUR
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
