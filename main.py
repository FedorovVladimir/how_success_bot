import telebot
import datetime

from Subject import Subject
from Task import Task

SUBJECT_NOT_FOUND = -1
DEFAULT_TEXT = 'Такого пока не умею'
bot = telebot.TeleBot('1073761581:AAF_Bf42Qit5PkRbrQbWf7yfprVogQMeemw')

subjects = [
    Subject('Программирование параллельных процессов', [
        Task("Потоки и отдельные приложения", False),
        Task("Читатели-писатели потребитьели-производители", False),
        Task("Сетевое взаимодействие", False),
        Task("Сервер системы", False),
        Task("MPI", False)
    ]),
    Subject('Методы вычислений', [
        Task("Метод наискорейшего спуска", False)
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
    bot.send_message(message.chat.id, 'Привет, это 3CRASBS!\nВыберите предмет для просмотра долгов.', reply_markup=subjectKeyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    info(message.from_user.username, message.text)

    n = SUBJECT_NOT_FOUND
    for i in range(len(subjects)):
        if message.text == subjects[i].name:
            n = i
            break

    text = DEFAULT_TEXT
    keys = telebot.types.InlineKeyboardMarkup()
    if n != SUBJECT_NOT_FOUND:
        noDoneTasks = list(filter(lambda t: t.done == False, subjects[n].tasks))
        text = 'Ещё ' + str(len(noDoneTasks)) + '!'
        if len(noDoneTasks) > 0:
            text += '\nНажмите на название работы которую вы сдали для отметки.'
        for i in range(len(noDoneTasks)):
            button = telebot.types.InlineKeyboardButton(
                text=subjects[n].tasks[i].name,
                callback_data="doneTask " + str(n) + " " + str(i))
            keys.add(button)
    bot.send_message(message.chat.id, text, reply_markup=keys)


@bot.callback_query_handler(func=lambda c: True)
def call_back(c):
    commands = c.data.split()
    info(c.from_user.username, commands)
    if commands[0] == "doneTask":
        subject = subjects[int(commands[1])]
        task = subject.tasks[int(commands[2])]
        task.done = True
        bot.send_message(c.message.chat.id, subject.name + "\n" + task.name + "\nСделана!")


bot.polling()
