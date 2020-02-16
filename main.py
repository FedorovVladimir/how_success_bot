import telebot
import datetime

from Subject import Subject
from Task import Task

SUBJECT_NOT_FOUND = -1
DEFAULT_TEXT = 'Такого пока не умею'
bot = telebot.TeleBot('1073761581:AAF_Bf42Qit5PkRbrQbWf7yfprVogQMeemw')


subjects = [
    Subject('Программирование параллельных процессов', [
        Task("Метод наискорейшего спуска", False)
    ]),
    Subject('Методы вычислений', [
        Task("Потоки и отдельные приложения", False),
        Task("Читатели-писатели потребитьели производители", False),
        Task("Сетевое взаимодействие", False),
        Task("Сервер системы", False),
        Task("MPI", False)
    ])
]


subjectKeyboard = telebot.types.ReplyKeyboardMarkup()
for subject in subjects:
    subjectKeyboard.add(subject.name)


def info(user, text):
    print(datetime.datetime.now(), "@" + user, text)


@bot.message_handler(commands=['start'])
def start_message(message):
    info(message.from_user.username, "/start")
    bot.send_message(message.chat.id, 'Привет, это 3CRASBS!', reply_markup=subjectKeyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    info(message.from_user.username, message.text)

    n = SUBJECT_NOT_FOUND
    for i in range(len(subjects)):
        if message.text == subjects[i].name:
            n = i
            break

    text = DEFAULT_TEXT
    if n != SUBJECT_NOT_FOUND:
        text = 'Ещё ' + str(len(subjects[n].tasks)) + ' !\n'
        for task in subjects[n].tasks:
            text += task.name + "\n"
    bot.send_message(message.chat.id, text)


bot.polling()
