import unittest
from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):
    def setUp(self):
        """Инициализация объектов для тестов."""
        self.vacancy1 = Vacancy(
            title="Python Developer",
            url="http://example.com/python",
            salary_from=100000,
            salary_to=150000,
            description="Работа с Python."
        )
        self.vacancy2 = Vacancy(
            title="Java Developer",
            url="http://example.com/java",
            salary_from=120000,
            salary_to=180000,
            description="Работа с Java."
        )
        self.vacancy3 = Vacancy(
            title="No Salary Developer",
            url="http://example.com/nosalary",
            salary_from=None,
            salary_to=None,
            description="Описание вакансии без зарплаты."
        )

    def test_initialization(self):
        """Тест: проверка корректной инициализации объекта."""
        self.assertEqual(self.vacancy1.get_title(), "Python Developer")
        self.assertEqual(self.vacancy1.get_url(), "http://example.com/python")
        self.assertEqual(self.vacancy1.get_salary_from(), 100000)
        self.assertEqual(self.vacancy1.get_salary_to(), 150000)
        self.assertEqual(self.vacancy1.get_description(), "Работа с Python.")

    def test_average_salary(self):
        """Тест: проверка расчета средней зарплаты."""
        self.assertEqual(self.vacancy1.average_salary(), 125000.0)
        self.assertEqual(self.vacancy2.average_salary(), 150000.0)
        self.assertIsNone(self.vacancy3.average_salary())

    def test_comparison(self):
        """Тест: проверка операций сравнения вакансий."""
        self.assertTrue(self.vacancy2 > self.vacancy1)  # 150000 > 125000
        self.assertTrue(self.vacancy1 < self.vacancy2)  # 125000 < 150000
        self.assertTrue(self.vacancy1 <= self.vacancy2)  # 125000 <= 150000
        self.assertFalse(self.vacancy1 == self.vacancy2)  # Средние зарплаты не равны
        self.assertTrue(self.vacancy3 < self.vacancy1)  # None < 125000
        self.assertFalse(self.vacancy3 > self.vacancy1)  # None > 125000
        self.assertTrue(self.vacancy3 <= self.vacancy1)  # None <= 125000
        self.assertTrue(self.vacancy3 >= self.vacancy3)  # None >= None

    def test_validation_success(self):
        """Тест: проверка успешной валидации входных данных."""
        vacancy = Vacancy(
            title="Go Developer",
            url="http://example.com/go",
            salary_from=80000,
            salary_to=120000,
            description="Работа с Go."
        )
        self.assertEqual(vacancy.get_title(), "Go Developer")
        self.assertEqual(vacancy.get_url(), "http://example.com/go")
        self.assertEqual(vacancy.get_salary_from(), 80000)
        self.assertEqual(vacancy.get_salary_to(), 120000)
        self.assertEqual(vacancy.get_description(), "Работа с Go.")

    def test_validation_failure(self):
        """Тест: проверка ошибок валидации входных данных."""
        with self.assertRaises(ValueError):
            Vacancy(title="", url="http://example.com", salary_from=100000, salary_to=200000, description="Описание.")
        with self.assertRaises(ValueError):
            Vacancy(title="Developer", url="", salary_from=100000, salary_to=200000, description="Описание.")
        with self.assertRaises(ValueError):
            Vacancy(title="Developer", url="invalid-url", salary_from=100000, salary_to=200000, description="Описание.")
        with self.assertRaises(ValueError):
            Vacancy(title="Developer", url="http://example.com", salary_from=-5000, salary_to=200000, description="Описание.")
        with self.assertRaises(ValueError):
            Vacancy(title="Developer", url="http://example.com", salary_from=100000, salary_to=-2000, description="Описание.")
        with self.assertRaises(ValueError):
            Vacancy(title="Developer", url="http://example.com", salary_from=100000, salary_to=200000, description="")

    def test_to_dict(self):
        """Тест: проверка преобразования объекта в словарь."""
        expected_dict = {
            'title': "Python Developer",
            'url': "http://example.com/python",
            'salary_from': 100000,
            'salary_to': 150000,
            'description': "Работа с Python."
        }
        self.assertEqual(self.vacancy1.to_dict(), expected_dict)

    def test_repr(self):
        """Тест: проверка строкового представления объекта."""
        expected_repr = (
            "Vacancy(title='Python Developer', url='http://example.com/python', "
            "salary_from=100000, salary_to=150000, description='Работа с Python....')"
        )
        self.assertEqual(repr(self.vacancy1), expected_repr)


if __name__ == "__main__":
    unittest.main()
