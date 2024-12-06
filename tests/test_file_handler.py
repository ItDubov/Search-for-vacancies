import unittest
import os
from src.file_handler import JSONFileHandler


class TestJSONFileHandler(unittest.TestCase):

    def setUp(self):
        """Создаем временный файл для тестов."""
        self.test_filename = "test_vacancies.json"
        self.handler = JSONFileHandler(self.test_filename)

    def tearDown(self):
        """Удаляем временный файл после тестов."""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

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
