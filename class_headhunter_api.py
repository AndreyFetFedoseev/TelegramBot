from abc import ABC, abstractmethod

import requests


class AbstractHH(ABC):
    """
    Абстрактный класс для работы с API HeadHunter
    """

    @abstractmethod
    def load_vacancies(self, keyword, city):
        pass


class HH(AbstractHH):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100, 'area': 1}
        self.vacancies = []

    def load_vacancies(self, keyword, city):
        """
        Получение списка вакансий по ключевому слову и выбранному городу
        :param keyword: str
        :param city: str
        :return: list
        """
        self.params['text'] = keyword
        self.params['area'] = city
        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1
