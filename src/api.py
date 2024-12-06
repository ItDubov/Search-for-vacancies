from abc import ABC, abstractmethod
import requests
from typing import List


class JobPlatformAPI(ABC):
    """
    Абстрактный класс для работы с API вакансий.
    """

    @abstractmethod
    def _connect_to_api(self, **kwargs) -> requests.Response:
        """
        Подключается к API сервиса. Реализация зависит от платформы.
        :param kwargs: Параметры подключения.
        :return: Ответ от API.
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str, pages: int = 1) -> List[dict]:
        """
        Получает список вакансий с платформы.
        :param keyword: Ключевое слово для поиска вакансий.
        :param pages: Количество страниц для запроса.
        :return: Список вакансий в формате словарей.
        """
        pass


class HeadHunterAPI(JobPlatformAPI):
    """
    Класс для работы с API HeadHunter, наследуется от JobPlatformAPI.
    """
    BASE_URL = "https://api.hh.ru/vacancies"

    def _connect_to_api(self, **kwargs) -> requests.Response:
        """
        Приватный метод подключения к API hh.ru.
        :param kwargs: Параметры подключения (например, text, page, per_page).
        :return: Ответ от API hh.ru.
        """
        try:
            response = requests.get(self.BASE_URL, params=kwargs)
            if response.status_code == 200:
                return response
            else:
                raise ValueError(
                    f"Ошибка подключения к API: статус-код {response.status_code} — {response.reason}"
                )
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка соединения с API hh.ru: {e}")

    def get_vacancies(self, keyword: str, pages: int = 1) -> List[dict]:
        """
        Метод получения вакансий с hh.ru.
        :param keyword: Ключевое слово для поиска вакансий.
        :param pages: Количество страниц для обработки.
        :return: Список вакансий (словарей) из API hh.ru.
        """
        vacancies = []

        for page in range(pages):
            # Подготовка параметров запроса
            params = {
                "text": keyword,
                "per_page": 50,  # Максимальное количество вакансий на странице
                "page": page,
            }

            # Вызов приватного метода подключения
            response = self._connect_to_api(**params)

            # Извлечение данных из ответа
            items = response.json().get("items", [])
            vacancies.extend(items)

        return vacancies
