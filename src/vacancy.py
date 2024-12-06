from typing import Union


class Vacancy:
    """
    Класс для работы с вакансиями.
    Используется для хранения информации о вакансиях и сравнения по зарплате.
    """

    __slots__ = ("_title", "_url", "_salary_from", "_salary_to", "_description")

    def __init__(self, title: str, url: str, salary_from: Union[int, None], salary_to: Union[int, None], description: str):
        """
        Инициализация экземпляра вакансии с валидацией данных.
        :param title: Название вакансии.
        :param url: Ссылка на вакансию.
        :param salary_from: Нижняя граница зарплаты (None, если не указана).
        :param salary_to: Верхняя граница зарплаты (None, если не указана).
        :param description: Краткое описание вакансии.
        """
        self._title = self._validate_title(title)
        self._url = self._validate_url(url)
        self._salary_from = self._validate_salary(salary_from)
        self._salary_to = self._validate_salary(salary_to)
        self._description = self._validate_description(description)

    def __repr__(self):
        """
        Представление экземпляра класса.
        """
        return (
            f"Vacancy(title='{self._title}', url='{self._url}', "
            f"salary_from={self._salary_from}, salary_to={self._salary_to}, description='{self._description[:50]}...')"
        )

    def __eq__(self, other: "Vacancy"):
        """
        Проверка равенства вакансий по зарплате.
        """
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.average_salary() == other.average_salary()

    def __lt__(self, other: "Vacancy"):
        if not isinstance(other, Vacancy):
            return NotImplemented
        self_salary = self.average_salary()
        other_salary = other.average_salary()

        # Обработка случаев, когда одна или обе зарплаты равны None
        if self_salary is None:
            return other_salary is not None
        if other_salary is None:
            return False
        return self_salary < other_salary

    def __le__(self, other: "Vacancy"):
        if not isinstance(other, Vacancy):
            return NotImplemented
        self_salary = self.average_salary()
        other_salary = other.average_salary()

        if self_salary is None:
            return True
        if other_salary is None:
            return False
        return self_salary <= other_salary

    def __gt__(self, other: "Vacancy"):
        if not isinstance(other, Vacancy):
            return NotImplemented
        self_salary = self.average_salary()
        other_salary = other.average_salary()

        if other_salary is None:
            return self_salary is not None
        if self_salary is None:
            return False
        return self_salary > other_salary

    def __ge__(self, other: "Vacancy"):
        if not isinstance(other, Vacancy):
            return NotImplemented
        self_salary = self.average_salary()
        other_salary = other.average_salary()

        if other_salary is None:
            return True
        if self_salary is None:
            return False
        return self_salary >= other_salary

    def average_salary(self) -> Union[float, None]:
        """
        Рассчитывает среднюю зарплату вакансии, если указаны границы зарплаты.
        :return: Средняя зарплата или None, если данные отсутствуют.
        """
        if self._salary_from is not None and self._salary_to is not None:
            return (self._salary_from + self._salary_to) / 2
        if self._salary_from is not None:
            return float(self._salary_from)
        if self._salary_to is not None:
            return float(self._salary_to)
        return None

    # Геттеры для доступа к защищённым атрибутам

    def get_title(self) -> str:
        """
        Геттер для названия вакансии.
        """
        return self._title

    def get_url(self) -> str:
        """
        Геттер для URL вакансии.
        """
        return self._url

    def get_salary_from(self) -> Union[int, None]:
        """
        Геттер для нижней границы зарплаты.
        """
        return self._salary_from

    def get_salary_to(self) -> Union[int, None]:
        """
        Геттер для верхней границы зарплаты.
        """
        return self._salary_to

    def get_description(self) -> str:
        """
        Геттер для описания вакансии.
        """
        return self._description

    @staticmethod
    def _validate_title(title: str) -> str:
        """
        Приватный метод валидации названия вакансии.
        :param title: Название вакансии.
        :return: Валидное название.
        """
        if not title or not isinstance(title, str):
            raise ValueError("Название вакансии должно быть непустой строкой.")
        return title.strip()

    @staticmethod
    def _validate_url(url: str) -> str:
        """
        Приватный метод валидации ссылки на вакансию.
        :param url: URL вакансии.
        :return: Валидный URL.
        """
        if not url or not isinstance(url, str) or not url.startswith("http"):
            raise ValueError("URL вакансии должен быть валидной строкой, начинающейся с 'http'.")
        return url.strip()

    @staticmethod
    def _validate_salary(salary: Union[int, None]) -> Union[int, None]:
        """
        Приватный метод валидации зарплаты.
        :param salary: Размер зарплаты (может быть None).
        :return: Валидный размер зарплаты.
        """
        if salary is None:
            return None
        if not isinstance(salary, int) or salary < 0:
            raise ValueError("Зарплата должна быть положительным целым числом или None.")
        return salary

    @staticmethod
    def _validate_description(description: str) -> str:
        """
        Приватный метод валидации описания вакансии.
        :param description: Описание вакансии.
        :return: Валидное описание.
        """
        if not description or not isinstance(description, str):
            raise ValueError("Описание вакансии должно быть непустой строкой.")
        return description.strip()

    def to_dict(self) -> dict:
        """
        Преобразует объект вакансии в словарь.
        :return: Словарь с данными вакансии.
        """
        return {
            'title': self.get_title(),
            'url': self.get_url(),
            'salary_from': self.get_salary_from(),
            'salary_to': self.get_salary_to(),
            'description': self.get_description()
        }
