import telebot
import datetime


bot = telebot.TeleBot('1073761581:AAF_Bf42Qit5PkRbrQbWf7yfprVogQMeemw')


subjects = [
    'Программирование параллельных процессов',
    'Методы вычислений',
    'Методология программной инженерии',
    'Распределенные системы обработки информации',
    'Конструирование компиляторов',
    'Функциональные языки в разработки распределенных систем',
    'Интелектуальные технологии обработки изображений',
    'Научно-исследовательский семинар'
]


keyboard1 = telebot.types.ReplyKeyboardMarkup()
for subject in subjects:
    keyboard1.add(subject)


def info(user, text):
    print(datetime.datetime.now(), "@" + user, text)


@bot.message_handler(commands=['start'])
def start_message(message):
    info(message.from_user.username, "/start")
    bot.send_message(message.chat.id, 'Привет, это 3CRASBS!', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    info(message.from_user.username, message.text)


bot.polling()
