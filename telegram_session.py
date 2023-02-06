from session import Session
from game import Game
import telebot

bot = telebot.TeleBot('6198599634:AAH9hJiVmuu87zDsLqe89q3exuyzPSxNnTo', parse_mode=None)
session = Session()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Are you player? Send /accept")


@bot.message_handler(commands=['accept'])
def register_in_session(message):
    bot.send_message(message.chat.id, session.add(message.from_user.username))


@bot.message_handler(commands=['draw'])
def draw(message):
    pass

@bot.message_handler(commands=['buy'])
def buy(message):
    pass

@bot.message_handler(commands=['charge'])
def charge(message):
    pass

@bot.message_handler(commands=['inventory'])
def inventory(message):
    pass



bot.infinity_polling()
