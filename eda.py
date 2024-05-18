import telebot
from telebot import types
from db import *

API_TOKEN = '6737399651:AAEEKGEQhjhf7wh1ixeAd9jm71MP4Q5hjP8'  # Замените на свой API токен

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['eda'])
def eda(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item_calories = types.KeyboardButton('Добавить калории')
    item_water = types.KeyboardButton('Добавить воду')
    markup.add(item_calories, item_water)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

# Обработчик нажатия на кнопку "Добавить калории"
@bot.message_handler(func=lambda message: message.text == 'Добавить калории')
def add_calories(message):
    bot.reply_to(message, "Введите количество калорий:")
    bot.register_next_step_handler(message, process_calories_step)

def process_calories_step(message):
    try:
        calorie_count = int(message.text)
        new_nutrition = Nutrition(calorie_count=calorie_count)
        session.add(new_nutrition)
        session.commit()
        bot.reply_to(message, 'Количество калорий успешно добавлено в базу данных!')
    except ValueError:
        bot.reply_to(message, 'Пожалуйста, введите число.')

# Обработчик нажатия на кнопку "Добавить воду"
@bot.message_handler(func=lambda message: message.text == 'Добавить воду')
def add_water(message):
    bot.reply_to(message, "Введите количество воды:")
    bot.register_next_step_handler(message, process_water_step)

def process_water_step(message):
    try:
        water_quantity = int(message.text)
        new_nutrition = Nutrition(water_quantity=water_quantity)
        session.add(new_nutrition)
        session.commit()
        bot.reply_to(message, 'Количество воды успешно добавлено в базу данных!')
    except ValueError:
        bot.reply_to(message, 'Пожалуйста, введите число.')