import telebot
from telebot import types
from class_headhunter_api import HH
from class_job_vacancies import JobVacancy
from class_job_files import JobFiles

bot = telebot.TeleBot('5859808636:AAFmC9v8iOpYIV7CuY5HWwbqJBMzFTw4kpo')

keyword_vacancy = ''
country = ''
top_n = 1
salary_range = '0-200000'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}!\nВведите ключевое слово для поиска вакансии: ')
    bot.register_next_step_handler(message, get_keyword)


def get_keyword(message):
    global keyword_vacancy
    keyword_vacancy = message.text.lower()
    bot.send_message(message.chat.id, 'Введите в каком городе искать вакансии: ')
    bot.register_next_step_handler(message, get_country)
    return keyword_vacancy


def get_country(message):
    global country
    country = message.text.capitalize()
    bot.send_message(message.chat.id, 'Введите кол-во вакансий для вывода в топ: ')
    bot.register_next_step_handler(message, get_top_n)
    return country


def get_top_n(message):
    global top_n
    top_n = int(message.text)
    bot.send_message(message.chat.id, 'Введите диапазон зарплат(Пример: 100000-150000): ')
    bot.register_next_step_handler(message, get_salary_range)
    return top_n


# def get_salary_range(message):
#     global keyword_vacancy
#     global country
#     global top_n
#     global salary_range
#     print(country)
#     print(top_n)
#     print(keyword_vacancy)


def get_salary_range(message):
    global salary_range
    salary_range = message.text
    # bot.register_next_step_handler(message, user_interaction(message, keyword_vacancy, country, top_n, salary_range))
    bot.send_message(message.chat.id, 'Для поиска введите "Z"')
    bot.register_next_step_handler(message, user_interaction)
    return salary_range


# @bot.message_handler(commands=['start'])
# def hello(message):
#     button = types.ReplyKeyboardMarkup()
#     but1 = types.KeyboardButton('Поиск вакансий')
#     button.row(but1)
#     bot.send_message(message.chat.id,
#                      f'Здравствуйте, {message.from_user.first_name}!', reply_markup=button)
#     # bot.send_message(message.chat.id, message) \nВведите ключевое слово для поиска вакансии
#     bot.register_next_step_handler(message, on_click)
#
#
# def on_click(message):
#     if message.text == 'Поиск вакансий':
#         # keyword_vacancy = message.text
#         bot.send_message(message.chat.id, 'Выбери город для поиска вакансий')
#         bot.register_next_step_handler()
#     # return keyword_vacancy


# @bot.message_handler()
def user_interaction(message):
    """
    Функция для взаимодействия с пользователем
    """
    # Создание экземпляра класса для работы с API сайта HeadHunter
    head_hunter_api = HH()
    global keyword_vacancy
    global country
    global top_n
    global salary_range
    # Запрашиваем у пользователя параметры для поиска и обработки списка вакансий
    # keyword = keyword_vacancy.text.lower()
    keyword = keyword_vacancy
    # country = 'Барнаул'
    # country = input('Введите в каком городе искать вакансии: ').capitalize()
    # top_n = int(input('Введите кол-во вакансий для вывода в топ: '))
    # top_n = 3
    # salary_range = input('Введите диапазон зарплат(Пример: 100000-150000): ')
    # salary_range = '0-200000'

    # Загрузка словаря городов из файла в формате JSON
    city = JobFiles.load_files('country.json')

    # Получение вакансий с hh.ru в формате JSON
    head_hunter_api.load_vacancies(keyword, city[country])

    # Сохранение списка вакансий с определенного города в json файл
    JobFiles.save_vacancies('data_vacancies.json', head_hunter_api.vacancies)

    # Обработка списка вакансий
    list_vacancies = JobVacancy.get_list_vacancy('data_vacancies.json')
    selection_vacancies_by_salary = JobVacancy.selection_of_vacancies(list_vacancies, salary_range)
    sort_top_vacancies = JobVacancy.sorted_top_vacancy(selection_vacancies_by_salary, top_n)
    a = JobVacancy.print_top_vacancies(sort_top_vacancies, selection_vacancies_by_salary)
    print(a)
    bot.send_message(message.chat.id, a)
    JobVacancy.count_vacancies = 0


# if __name__ == "__main__":
#     user_interaction()


bot.infinity_polling()
