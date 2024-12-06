from typing import List
from src.vacancy import Vacancy
from src.file_handler import JSONFileHandler
from src.api import HeadHunterAPI


def display_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Функция для вывода вакансий в человекочитаемом формате.
    :param vacancies: Список вакансий для отображения.
    """
    if not vacancies:
        print("Нет вакансий для отображения.")
        return

    print(f"Найдено {len(vacancies)} вакансий:")
    for idx, vacancy in enumerate(vacancies, 1):
        print(f"{idx}. {vacancy.get_title()}")  # Используем геттер get_title()
        print(f"   Ссылка: {vacancy.get_url()}")  # Используем геттер get_url()
        print(f"   Зарплата: {vacancy.get_salary_from()} - {vacancy.get_salary_to()}")  # Используем геттеры
        print(f"   Описание: {vacancy.get_description()}")  # Используем геттер get_description()
        print("-" * 2000)


def user_interaction() -> None:
    """
    Функция для взаимодействия с пользователем.
    Позволяет пользователю искать вакансии, фильтровать их, получать топ по зарплате и работать с данными.
    """
    # Пример использования HeadHunter API для поиска вакансий
    hh_api = HeadHunterAPI()

    # Получение поискового запроса от пользователя
    search_query = input("Введите поисковый запрос для вакансий (например, Python): ").strip()
    if not search_query:
        print("Запрос не может быть пустым!")
        return

    # Получение данных от API
    print(f"Ищу вакансии по запросу: {search_query}...")
    vacancies_data = hh_api.get_vacancies(search_query)

    # Преобразование полученных данных в список объектов Vacancy
    vacancies = [
        Vacancy(
            vacancy['name'],
            vacancy['url'],
            vacancy['salary'].get('from') if vacancy.get('salary') else None,  # Получаем нижнюю границу зарплаты
            vacancy['salary'].get('to') if vacancy.get('salary') else None,  # Получаем верхнюю границу зарплаты
            vacancy.get('description') or vacancy.get('snippet', {}).get('requirement') or 'Нет описания'  # Если нет описания, задаем значение по умолчанию
        )
        for vacancy in vacancies_data
    ]

    # Показываем все найденные вакансии
    display_vacancies(vacancies)

    # Запрос пользователя для сортировки вакансий по зарплате
    try:
        top_n = int(input("Введите количество вакансий для вывода в топ по зарплате: "))
        if top_n <= 0:
            print("Введите положительное число для количества вакансий.")
            return
    except ValueError:
        print("Неверный формат числа!")
        return

    # Сортировка вакансий по зарплате
    vacancies.sort(key=lambda v: v.get_salary_from() if v.get_salary_from() is not None else 0, reverse=True)

    # Получение топ N вакансий
    top_vacancies = vacancies[:top_n]
    print("\nТоп вакансий по зарплате:")
    display_vacancies(top_vacancies)

    # Запрос ключевых слов для фильтрации вакансий по описанию
    filter_words = input("\nВведите ключевые слова для фильтрации вакансий по описанию: ").strip().split()

    if filter_words:
        # Фильтрация вакансий по ключевым словам
        filtered_vacancies = [
            vacancy for vacancy in vacancies if
            any(word.lower() in vacancy.get_description().lower() for word in filter_words)
        ]
        print("\nВакансии, соответствующие ключевым словам:")
        display_vacancies(filtered_vacancies)
    else:
        print("Фильтрация по ключевым словам не была выполнена, так как ключевые слова не введены.")

    # Сохранение вакансий в файл
    save_to_file = input("\nХотите сохранить вакансии в файл? (Да/Нет): ").strip().lower()
    if save_to_file == 'Да':
        filename = input("Введите имя файла для сохранения вакансий (например, vacancies.json): ").strip()
        file_handler = JSONFileHandler(filename)  # Передаем имя файла для сохранения
        for vacancy in vacancies:
            file_handler.add_data(vacancy.to_dict())
        print(f"Вакансии успешно сохранены в файл {filename}.")

    print("Завершение программы.")