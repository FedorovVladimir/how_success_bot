import telebot
import datetime


bot = telebot.TeleBot('1073761581:AAF_Bf42Qit5PkRbrQbWf7yfprVogQMeemw')


def info(user, text):
    print(datetime.datetime.now(), "@" + user, text)


@bot.message_handler(commands=['start'])
def start_message(message):
    info(message.from_user.username, "/start")
    bot.send_message(message.chat.id, 'Привет, это 3CRASBS!')


@bot.message_handler(content_types=['text'])
def send_text(message):
    info(message.from_user.username, message.text)
    if message.text == 'Привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text == 'Пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')


bot.polling()
