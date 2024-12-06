import unittest
import os
from src.file_handler import JSONFileHandler, TextFileHandler


class TestJSONFileHandler(unittest.TestCase):


    def setUp(self):
        """Создаем временный файл для тестов."""
        self.test_filename = "test_vacancies.json"
        self.handler = JSONFileHandler(self.test_filename)


    def tearDown(self):
        """Удаляем временный файл после тестов."""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)


    def test_get_data_empty(self):
        """Тест: получение данных из пустого файла."""
        data = self.handler.get_data()
        self.assertEqual(data, [])


    def test_add_duplicate_data(self):
        """Тест: проверка, что дублирующие записи не добавляются."""
        vacancy = {"title": "Python Developer", "salary": 100000}
        self.handler.add_data(vacancy)
        self.handler.add_data(vacancy)  # Добавляем второй раз

        data = self.handler.get_data()
        self.assertEqual(len(data), 1)  # Должно быть только одна запись


    def test_delete_data(self):
        """Тест: удаление данных по критерию."""
        vacancies = [
            {"title": "Python Developer", "salary": 100000},
            {"title": "Java Developer", "salary": 120000},
        ]
        for vacancy in vacancies:
            self.handler.add_data(vacancy)

        self.handler.delete_data({"title": "Python Developer"})
        data = self.handler.get_data()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Java Developer")


    def test_delete_nonexistent_data(self):
        """Тест: удаление данных, которые отсутствуют в файле."""
        vacancy = {"title": "Python Developer", "salary": 100000}
        self.handler.add_data(vacancy)

        self.handler.delete_data({"title": "Java Developer"})
        data = self.handler.get_data()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Python Developer")


class TestTextFileHandler(unittest.TestCase):


    def setUp(self):
        """Создаем временный текстовый файл для тестов."""
        self.test_filename = "test_vacancies.txt"
        self.handler = TextFileHandler(self.test_filename)


    def tearDown(self):
        """Удаляем временный файл после тестов."""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)


    def test_get_data_empty(self):
        """Тест: получение данных из пустого текстового файла."""
        data = self.handler.get_data()
        self.assertEqual(data, [])


    def test_add_data(self):
        """Тест: добавление строки в файл."""
        vacancy = "Python Developer"
        self.handler.add_data(vacancy)

        data = self.handler.get_data()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].strip(), vacancy)


    def test_add_multiple_data(self):
        """Тест: добавление нескольких строк в файл."""
        vacancies = ["Python Developer", "Java Developer", "C++ Developer"]
        for vacancy in vacancies:
            self.handler.add_data(vacancy)

        data = self.handler.get_data()
        self.assertEqual(len(data), 3)
        self.assertEqual([line.strip() for line in data], vacancies)


    def test_delete_data(self):
        """Тест: удаление строки из файла."""
        vacancies = ["Python Developer", "Java Developer", "C++ Developer"]
        for vacancy in vacancies:
            self.handler.add_data(vacancy)

        self.handler.delete_data("Java Developer")
        data = self.handler.get_data()
        self.assertEqual(len(data), 2)
        self.assertNotIn("Java Developer", [line.strip() for line in data])


    def test_delete_nonexistent_data(self):
        """Тест: удаление строки, которой нет в файле."""
        vacancies = ["Python Developer", "Java Developer"]
        for vacancy in vacancies:
            self.handler.add_data(vacancy)

        self.handler.delete_data("C++ Developer")
        data = self.handler.get_data()
        self.assertEqual(len(data), 2)
        self.assertEqual([line.strip() for line in data], vacancies)
