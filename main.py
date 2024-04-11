import telebot
from telebot import types
from telebot import util

from class_headhunter_api import HH
from class_job_vacancies import JobVacancy
from class_job_files import JobFiles

from config import TOKEN

bot = telebot.TeleBot(TOKEN)

keyword_vacancy = ''
country = ''
top_n = 1
salary_range = '0-200000'

# Загрузка словаря городов из файла в формате JSON
city = JobFiles.load_files('country.json')


# Запрашиваем у пользователя параметры для поиска и обработки списка вакансий
@bot.message_handler(commands=['start', 'Следующий запрос'])
def start(message):
    bot.send_message(message.chat.id,
                     f'Здравствуйте, {message.from_user.first_name}!\nВведите ключевое слово для поиска вакансии: ')
    bot.register_next_step_handler(message, get_keyword)


def get_keyword(message):
    global keyword_vacancy
    keyword_vacancy = message.text.lower()
    bot.send_message(message.chat.id, 'Введите в каком городе искать вакансии: ')
    bot.register_next_step_handler(message, get_country)
    return keyword_vacancy


def get_country(message):
    global country
    global city
    country = message.text.capitalize()
    try:
        if city[country]:
            bot.send_message(message.chat.id, 'Введите кол-во вакансий для вывода в топ: ')
            bot.register_next_step_handler(message, get_top_n)
        return country
    except KeyError:
        bot.send_message(message.chat.id, f'Такого города нет.\nВведите в каком городе искать вакансии: ')
        bot.register_next_step_handler(message, get_country)


def get_top_n(message):
    global top_n
    try:
        top_n = int(message.text)
        bot.send_message(message.chat.id, 'Введите диапазон зарплат(Пример: 100000-150000): ')
        bot.register_next_step_handler(message, get_salary_range)
        return top_n
    except ValueError:
        bot.send_message(message.chat.id, 'Необходимо ввести число.\nВведите кол-во вакансий для вывода в топ: ')
        bot.register_next_step_handler(message, get_top_n)


def get_salary_range(message):
    global salary_range
    salary_range = message.text
    try:
        if len([x for x in salary_range.split('-') if int(x) >= 0]) == 2:
            user_interaction(message)
            return salary_range
        else:
            bot.send_message(message.chat.id,
                             f'Неверно введен диапазон.\nВведите диапазон зарплат(Пример: 100000-150000): ')
            bot.register_next_step_handler(message, get_salary_range)
    except ValueError:
        bot.send_message(message.chat.id,
                         f'Неверно введен диапазон.\nВведите диапазон зарплат(Пример: 100000-150000): ')
        bot.register_next_step_handler(message, get_salary_range)


def user_interaction(message):
    """
    Функция для взаимодействия с пользователем
    """
    global keyword_vacancy
    global country
    global top_n
    global salary_range
    global city

    # Создание экземпляра класса для работы с API сайта HeadHunter
    head_hunter_api = HH()

    # Получение вакансий с hh.ru в формате JSON
    head_hunter_api.load_vacancies(keyword_vacancy, city[country])

    # Сохранение списка вакансий с определенного города в json файл
    JobFiles.save_vacancies('data_vacancies.json', head_hunter_api.vacancies)

    # Обработка списка вакансий
    list_vacancies = JobVacancy.get_list_vacancy('data_vacancies.json')
    selection_vacancies_by_salary = JobVacancy.selection_of_vacancies(list_vacancies, salary_range)
    sort_top_vacancies = JobVacancy.sorted_top_vacancy(selection_vacancies_by_salary, top_n)
    vacancy = JobVacancy.print_top_vacancies(sort_top_vacancies, selection_vacancies_by_salary)
    print(vacancy)
    JobVacancy.count_vacancies = 0
    button = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn2 = types.KeyboardButton('Следующий запрос')
    button.row(btn2)
    for mes in util.smart_split(vacancy, 10000):
        bot.send_message(message.chat.id, mes, reply_markup=button)
    bot.register_next_step_handler(message, start)


bot.infinity_polling()
