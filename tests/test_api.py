import unittest
from unittest.mock import patch, Mock
from src.api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):
    """Тесты для класса HeadHunterAPI."""

    @patch("src.api.requests.get")
    def test_connect_to_api_success(self, mock_get):
        """Тест успешного подключения к API hh.ru."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        response = api._connect_to_api(text="Python")

        self.assertEqual(response.status_code, 200)
        mock_get.assert_called_once_with(api.BASE_URL, params={"text": "Python"})

    @patch("src.api.requests.get")
    def test_connect_to_api_failure(self, mock_get):
        """Тест ошибки подключения к API hh.ru."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_get.return_value = mock_response

        api = HeadHunterAPI()

        with self.assertRaises(ValueError) as context:
            api._connect_to_api(text="Python")
        self.assertIn("Ошибка подключения к API", str(context.exception))
        mock_get.assert_called_once_with(api.BASE_URL, params={"text": "Python"})

    @patch("src.api.requests.get")
    def test_get_vacancies(self, mock_get):
        """Тест получения списка вакансий с hh.ru."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {"id": "1", "name": "Python Developer"},
                {"id": "2", "name": "Data Scientist"},
            ]
        }
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        vacancies = api.get_vacancies(keyword="Python", pages=1)

        self.assertEqual(len(vacancies), 2)
        self.assertEqual(vacancies[0]["name"], "Python Developer")
        self.assertEqual(vacancies[1]["name"], "Data Scientist")
        mock_get.assert_called_once_with(
            api.BASE_URL,
            params={"text": "Python", "per_page": 50, "page": 0},
        )

    @patch("src.api.requests.get")
    def test_get_vacancies_multiple_pages(self, mock_get):
        """Тест получения вакансий с нескольких страниц."""
        mock_response_page1 = Mock()
        mock_response_page1.status_code = 200
        mock_response_page1.json.return_value = {
            "items": [{"id": "1", "name": "Python Developer"}]
        }

        mock_response_page2 = Mock()
        mock_response_page2.status_code = 200
        mock_response_page2.json.return_value = {
            "items": [{"id": "2", "name": "Data Scientist"}]
        }

        mock_get.side_effect = [mock_response_page1, mock_response_page2]

        api = HeadHunterAPI()
        vacancies = api.get_vacancies(keyword="Python", pages=2)

        self.assertEqual(len(vacancies), 2)
        self.assertEqual(vacancies[0]["name"], "Python Developer")
        self.assertEqual(vacancies[1]["name"], "Data Scientist")
        self.assertEqual(mock_get.call_count, 2)
        mock_get.assert_any_call(api.BASE_URL, params={"text": "Python", "per_page": 50, "page": 0})
        mock_get.assert_any_call(api.BASE_URL, params={"text": "Python", "per_page": 50, "page": 1})
