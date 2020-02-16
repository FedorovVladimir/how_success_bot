import telebot
import datetime
import requests
import json

SELECT_OUT_SUBJECT = False
SELECT_IN_SUBJECT = False
SUBJECT_NOT_FOUND = -1
DEFAULT_TEXT = 'Такого пока не умею'
bot = telebot.TeleBot('975464059:AAH5gERiAoJ7IvRaIOXyJvHPGX61ZDPwE6M')

biletikBaseUrl = 'https://biletik.ext-system.com/client-api'
subject_id_out = -1
subject_id_in = -1

mainMenuItems = [
    'Выбрать пункт отправления',
    'Выбрать пункт прибытия',
    'Посмотреть рейсы',
]
mainMenuKeyboard = telebot.types.ReplyKeyboardMarkup()
for mainMenuItem in mainMenuItems:
    mainMenuKeyboard.add(mainMenuItem)


def info(user, text):
    print(datetime.datetime.now(), "@" + user, text)


@bot.message_handler(commands=['start'])
def start_message(message):
    info(message.from_user.username, "/start")
    bot.send_message(message.chat.id,
                     'Привет, это biletik_online_bot!\nПоехали!)',
                     reply_markup=mainMenuKeyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    global SELECT_OUT_SUBJECT
    global SELECT_IN_SUBJECT
    info(message.from_user.username, message.text)

    n = SUBJECT_NOT_FOUND
    for i in range(len(mainMenuItems)):
        if message.text == mainMenuItems[i]:
            n = i
            break

    if n != SUBJECT_NOT_FOUND:
        if n == 0:
            SELECT_OUT_SUBJECT = True
            bot.send_message(message.chat.id, "Введите часть или полное название пункта отправления.")
            return
        elif n == 1:
            SELECT_IN_SUBJECT = True
            bot.send_message(message.chat.id, "Введите часть или полное название пункта прибытия.")
            return
        elif n == 2:
            subjects_json = requests.get(
                biletikBaseUrl +
                '/v2/trips?date=16.02.2020&departureType=Point&destinationType=Point&idDeparture='
                + str(subject_id_out) +
                '&idDestination=' + str(subject_id_in))
            trips = json.loads(subjects_json.text)['data']
            keys = telebot.types.InlineKeyboardMarkup()
            for trip in trips:
                button = telebot.types.InlineKeyboardButton(
                    text=trip['route']['name'] + '\nСвободных мест: ' + str(trip['places']['free']),
                    callback_data="test")
                keys.add(button)
            bot.send_message(message.chat.id, "Рейсы на сегодня.", reply_markup=keys)
            return

    if SELECT_OUT_SUBJECT is True:
        SELECT_OUT_SUBJECT = False
        term = message.text
        subjects_json = requests.get(biletikBaseUrl + "/subjects/departure?term=" + term)
        subjects = json.loads(subjects_json.text)['data']
        keys = telebot.types.InlineKeyboardMarkup()
        for subject in subjects:
            button = telebot.types.InlineKeyboardButton(
                text=subject['name'],
                callback_data="departure " + str(subject['id']))
            keys.add(button)
        bot.send_message(message.chat.id, 'Выберите пункт отправления', reply_markup=keys)

    if SELECT_IN_SUBJECT is True:
        SELECT_IN_SUBJECT = False
        term = message.text
        subjects_json = requests.get(biletikBaseUrl + "/subjects/destination?term=" + term)
        subjects = json.loads(subjects_json.text)['data']
        keys = telebot.types.InlineKeyboardMarkup()
        for subject in subjects:
            button = telebot.types.InlineKeyboardButton(
                text=subject['name'],
                callback_data="destination " + str(subject['id']))
            keys.add(button)
        bot.send_message(message.chat.id, 'Выберите пункт отправления', reply_markup=keys)


@bot.callback_query_handler(func=lambda c: True)
def call_back(c):
    global subject_id_out
    global subject_id_in
    commands = c.data.split()
    info(c.from_user.username, commands)
    if commands[0] == "departure":
        subject_id_out = int(commands[1])
        bot.send_message(c.message.chat.id, 'Пункт отправления выбран')
    elif commands[0] == "destination":
        subject_id_in = int(commands[1])
        bot.send_message(c.message.chat.id, 'Пункт прибытия выбран')


bot.polling()
