import unittest
from unittest.mock import patch
from src.vacancy import Vacancy
from src.file_handler import JSONFileHandler
from src.utils import display_vacancies


class TestVacancyApp(unittest.TestCase):
    def setUp(self):
        """Создание набора тестовых вакансий."""
        self.vacancies = [
            Vacancy("Python Developer", "http://example.com/1", 100000, 150000, "Разработка на Python"),
            Vacancy("Java Developer", "http://example.com/2", 120000, 170000, "Разработка на Java"),
            Vacancy("C++ Developer", "http://example.com/3", 90000, 130000, "Разработка на C++"),
        ]
        self.empty_vacancies = []


    def test_display_vacancies_empty(self):
        """Тест: вывод для пустого списка вакансий."""
        with patch('builtins.print') as mock_print:
            display_vacancies(self.empty_vacancies)
            mock_print.assert_called_with("Нет вакансий для отображения.")


    def test_display_vacancies(self):
        """Тест: корректный вывод списка вакансий."""
        with patch('builtins.print') as mock_print:
            display_vacancies(self.vacancies)
            self.assertTrue(mock_print.called)
            mock_print.assert_any_call("1. Python Developer")
            mock_print.assert_any_call("2. Java Developer")
            mock_print.assert_any_call("3. C++ Developer")


    def test_vacancies_from_api(self):
        """Тест: преобразование данных API в объекты Vacancy."""
        api_data = [
            {
                "name": "Python Developer",
                "url": "http://example.com/1",
                "salary": {"from": 100000, "to": 150000},
                "description": "Разработка на Python",
            },
            {
                "name": "Java Developer",
                "url": "http://example.com/2",
                "salary": {"from": 120000, "to": 170000},
                "description": None,
            },
        ]
        vacancies = [
            Vacancy(
                vacancy['name'],
                vacancy['url'],
                vacancy['salary'].get('from') if vacancy.get('salary') else None,
                vacancy['salary'].get('to') if vacancy.get('salary') else None,
                vacancy.get('description') or "Нет описания",
            )
            for vacancy in api_data
        ]
        self.assertEqual(len(vacancies), 2)
        self.assertEqual(vacancies[0].get_title(), "Python Developer")
        self.assertEqual(vacancies[1].get_salary_to(), 170000)
        self.assertEqual(vacancies[1].get_description(), "Нет описания")


    def test_filter_vacancies_by_keywords(self):
        """Тест: фильтрация вакансий по ключевым словам."""
        keywords = ["Python", "C++"]
        filtered = [
            vacancy for vacancy in self.vacancies
            if any(word.lower() in vacancy.get_description().lower() for word in keywords)
        ]
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0].get_title(), "Python Developer")
        self.assertEqual(filtered[1].get_title(), "C++ Developer")


    def test_sort_vacancies_by_salary(self):
        """Тест: сортировка вакансий по нижней границе зарплаты."""
        sorted_vacancies = sorted(self.vacancies, key=lambda v: v.get_salary_from() or 0, reverse=True)
        self.assertEqual(sorted_vacancies[0].get_title(), "Java Developer")
        self.assertEqual(sorted_vacancies[1].get_title(), "Python Developer")
        self.assertEqual(sorted_vacancies[2].get_title(), "C++ Developer")
