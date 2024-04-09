import telebot
from telebot import types

bot = telebot.TeleBot('5859808636:AAFmC9v8iOpYIV7CuY5HWwbqJBMzFTw4kpo')

# @bot.message_handler(commands=['start'])
# def main(message):
#     button = types.InlineKeyboardMarkup()
#     bot.send_message(message.chat.id, 'Hello')


# @bot.message_handler()
# def info(message):
#     if message.text.lower() == 'id':
#         bot.reply_to(message, f'ID: {message.from_user.id}')


from class_headhunter_api import HH
from class_job_vacancies import JobVacancy
from class_job_files import JobFiles


@bot.message_handler()
def user_interaction(message):
    """
    Функция для взаимодействия с пользователем
    """
    # Создание экземпляра класса для работы с API сайта HeadHunter
    head_hunter_api = HH()

    # Запрашиваем у пользователя параметры для поиска и обработки списка вакансий
    keyword = message.text.lower()
    country = 'Барнаул'
    # country = input('Введите в каком городе искать вакансии: ').capitalize()
    # top_n = int(input('Введите кол-во вакансий для вывода в топ: '))
    top_n = 3
    # salary_range = input('Введите диапазон зарплат(Пример: 100000-150000): ')
    salary_range = '0-300000'

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


# if __name__ == "__main__":
#     user_interaction()


bot.polling(none_stop=True)
