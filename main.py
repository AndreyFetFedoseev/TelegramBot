import telebot

bot = telebot.TeleBot('5859808636:AAFmC9v8iOpYIV7CuY5HWwbqJBMzFTw4kpo')


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Hello')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')


bot.polling(none_stop=True)
