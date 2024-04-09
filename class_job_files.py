import json
from abc import ABC, abstractmethod


class AbstractJobFiles(ABC):

    @staticmethod
    @abstractmethod
    def load_files(json_file):
        pass

    @staticmethod
    @abstractmethod
    def save_vacancies(files, data):
        pass

    @staticmethod
    @abstractmethod
    def del_vacancy(data):
        pass


class JobFiles(AbstractJobFiles):
    """
    Класс для работы с файлами
    """

    @staticmethod
    def load_files(json_file):
        """
        Выгружает список вакансий из json файла
        :param json_file: str
        :return: data_vacancy
        """
        with open(json_file, 'r') as file:
            data_vacancy = json.load(file)
        return data_vacancy

    @staticmethod
    def save_vacancies(files, data):
        """
        Сохрнение списка вакансий в json файл (перезапись)
        :param files: str
        :param data: []
        """
        with open(files, 'w', encoding='utf-8') as file:
            json.dump(data, file)

    @staticmethod
    def del_vacancy(data):
        pass
