#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

from telebot import types
import telebot

API_TOKEN = '7152393012:AAGnC0py4t03xZ19-NL3QEWbI9u1OxFpQHk'

bot = telebot.TeleBot(API_TOKEN)
class UserState:
    def __init__(self):
        self.squats = 0

user_states = {}

def start_15(message):
    chat_id = message.chat.id
    if chat_id not in user_states:
        user_states[chat_id] = UserState()
    user_states[chat_id].squats += 15
    bot.reply_to(message, f"Добавлено 15 раз\nВсего преседаний - {user_states[chat_id].squats}")

def sbros_15(message):
    chat_id = message.chat.id
    if chat_id in user_states and user_states[chat_id].squats != 0:
        user_states[chat_id].squats = 0
        bot.reply_to(message, "Сброс преседаний выполнен. Всего преседаний - 0")
    else:
        bot.reply_to(message, "Преседания уже были сброшены.")

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("+15 раз")
    btn2 = types.KeyboardButton("Сброс преседаний")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Выберите опцию", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def button(message):
    if message.text == "+15 раз":
        start_15(message)
    elif message.text == "Сброс преседаний":
        sbros_15(message)

bot.infinity_polling()