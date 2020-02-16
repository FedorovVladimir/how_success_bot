import telebot

bot = telebot.TeleBot('1073761581:AAF_Bf42Qit5PkRbrQbWf7yfprVogQMeemw')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, это 3CRASBS!')


bot.polling()
