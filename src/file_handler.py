import os
import json
from abc import ABC, abstractmethod
from typing import List, Dict


class FileHandler(ABC):
    """
    Абстрактный класс для работы с файлами.
    """

    @abstractmethod
    def get_data(self) -> List[Dict]:
        """
        Абстрактный метод получения данных из файла.
        :return: Список словарей с данными.
        """
        pass

    @abstractmethod
    def add_data(self, data: Dict) -> None:
        """
        Абстрактный метод добавления данных в файл.
        :param data: Данные для добавления.
        """
        pass

    @abstractmethod
    def delete_data(self, criteria: Dict) -> None:
        """
        Абстрактный метод удаления данных из файла по критерию.
        :param criteria: Критерий для удаления данных.
        """
        pass


class JSONFileHandler(FileHandler):
    """
    Класс для работы с JSON-файлами.
    """

    def __init__(self, filename: str = "vacancies.json"):
        """
        Инициализация экземпляра с именем файла.
        :param filename: Имя файла (по умолчанию "vacancies.json").
        """
        self._directory = "data"  # Папка для хранения файлов
        self._filename = os.path.join(self._directory, filename)

        # Создаем папку data, если ее нет
        if not os.path.exists(self._directory):
            os.makedirs(self._directory)

    def _read_file(self) -> List[Dict]:
        """
        Приватный метод чтения данных из JSON-файла.
        :return: Список словарей с данными.
        """
        try:
            with open(self._filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Возвращает пустой список, если файл не найден или поврежден

    def _write_file(self, data: List[Dict]) -> None:
        """
        Приватный метод записи данных в JSON-файл.
        :param data: Список словарей для записи.
        """
        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_data(self) -> List[Dict]:
        """
        Получение всех данных из файла.
        :return: Список словарей с данными.
        """
        return self._read_file()

    def add_data(self, data: Dict) -> None:
        """
        Добавление данных в JSON-файл без создания дублирующих записей.
        :param data: Словарь с данными для добавления.
        """
        all_data = self._read_file()
        if data not in all_data:  # Проверка на дублирование данных
            all_data.append(data)
            self._write_file(all_data)

    def delete_data(self, criteria: Dict) -> None:
        """
        Удаление данных из JSON-файла по критерию.
        :param criteria: Словарь с критериями для удаления (например, {"title": "Python Developer"}).
        """
        all_data = self._read_file()
        filtered_data = [
            entry for entry in all_data
            if not all(entry.get(k) == v for k, v in criteria.items())
        ]
        self._write_file(filtered_data)


# Пример использования
if __name__ == "__main__":
    handler = JSONFileHandler()
    handler.add_data({"title": "Python Developer", "salary": 150000})
    handler.add_data({"title": "Data Scientist", "salary": 200000})
    print("Вакансии:", handler.get_data())
    handler.delete_data({"title": "Python Developer"})
    print("После удаления:", handler.get_data())
