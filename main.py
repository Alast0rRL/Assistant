#!/usr/bin/python

from datetime import datetime
from sqlalchemy import func
import telebot
from telebot import types
from db import *
from eda import *

API_TOKEN = '6737399651:AAEEKGEQhjhf7wh1ixeAd9jm71MP4Q5hjP8'  # Замените на свой API токен

bot = telebot.TeleBot(API_TOKEN)

# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.reply_to(message, "Привет! Я бот для управления базой данных. "
#                           "Чтобы добавить заметку к человеку, нажмите /add_note. "
#                           "Чтобы добавить человека, нажмите /add_person. "
#                           "Чтобы вывести всех людей, нажмите /show_people.")



@bot.message_handler(commands=['start'])
def start(message):
    people = session.query(Person).all()
    if people:
        # Создаем клавиатуру с кнопками для каждого человека из базы данных
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for person in people:
            markup.add(types.KeyboardButton(person.name))
        markup.add(types.KeyboardButton("/add_person"))  # Добавляем кнопку "/add_person"
        bot.reply_to(message, "Выберите человека:", reply_markup=markup)
    else:
        bot.reply_to(message, "В базе данных нет ни одного человека.")
    
    bot.register_next_step_handler(message, chosen_person_step)
















global person_ID

@bot.message_handler(commands=['chosen_person'])
def chosen_person_command(message):
    # Запрашиваем у пользователя имя человека или его ID
    bot.reply_to(message, "Введите имя человека или его ID, для которого хотите просмотреть заметки:")
    
    # Устанавливаем состояние пользователя, чтобы следующее сообщение обрабатывалось как имя человека или его ID
    bot.register_next_step_handler(message, chosen_person_step)

def chosen_person_step(message):
    global person_ID  # Объявляем переменную как глобальную

    # Получаем ввод пользователя из сообщения
    input_text = message.text.strip()

    # Проверяем, является ли ввод числом (ID) или строкой (имя)
    if input_text.isdigit():
        # Если ввод является числом, ищем человека по ID
        person = session.query(Person).filter_by(id=int(input_text)).first()
        person_ID = input_text  # Присваиваем значение переменной
    else:
        # Если ввод не является числом, ищем человека по имени
        person = session.query(Person).filter_by(name=input_text).first()
        person_ID = person.id if person else None  # Присваиваем значение переменной

    if person:
        # Если человек найден, получаем все его заметки
        notes = person.notes
        if notes:
            response = f"Заметки для {person.name} (ID: {person.id}):\n"  # Включаем ID в сообщение
            for note in notes:
                response += f"Заметка {note.id}: {note.content}\n"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("/add_note"), types.KeyboardButton("/start"))
            bot.reply_to(message, response, reply_markup=markup)
        else:
            bot.reply_to(message, f"{person.name} (ID: {person.id}) не имеет заметок.")  # Включаем ID в сообщение            
    else:
        bot.reply_to(message, f"Человек с именем или ID '{input_text}' не найден.")

# Остальные функции остаются без изменений










@bot.message_handler(commands=['add_note'])
def add_note_to_person_step(message):
    # Проверяем, было ли установлено значение person_ID
    if person_ID is not None:
        # Если person_ID установлен, значит мы получили ID персоны в предыдущем шаге
        # Продолжаем обработку здесь
        handle_add_note_to_person_step(message)
    else:
        # Если person_ID не установлен, сообщаем об ошибке
        bot.reply_to(message, "Сначала выберите человека для добавления заметки.")

def handle_add_note_to_person_step(message):
    # Получаем ввод пользователя из сообщения
    input_text = message.text.strip()

    # Проверяем, является ли ввод числом (ID) или строкой (имя)
    if isinstance(person_ID, int):  # Используем isinstance для проверки типа
        # Если person_ID является числом, ищем человека по ID
        person = session.query(Person).filter_by(id=person_ID).first()
    else:
        # Если person_ID не является числом, сообщаем об ошибке
        bot.reply_to(message, "Ошибка: неверный идентификатор персоны.")
        return

    if person:
        # Если человек найден, запрашиваем содержимое заметки
        bot.reply_to(message, "Введите содержимое заметки:")
        
        # Устанавливаем состояние пользователя, чтобы следующее сообщение обрабатывалось как содержимое заметки
        bot.register_next_step_handler(message, lambda m: add_note_to_person_step2(m, person))
    else:
        bot.reply_to(message, f"Человек с ID '{person_ID}' не найден.")

def add_note_to_person_step2(message, person):
    # Получаем содержимое заметки из сообщения
    note_content = message.text.strip()

    # Создаем новый объект Note и связываем его с найденным человеком
    new_note = Note(content=note_content, person=person)

    # Добавляем заметку в сессию
    session.add(new_note)

    # Сохраняем изменения в базе данных
    session.commit()

    # Отправляем пользователю сообщение о успешном добавлении заметки
    bot.reply_to(message, f"Заметка успешно добавлена к {person.name}")








@bot.message_handler(commands=['add_person'])
def add_person_from_input(message):
    # Запрашиваем данные о человеке у пользователя
    bot.reply_to(message, "Введите имя человека:")
    
    # Устанавливаем состояние пользователя, чтобы следующее сообщение обрабатывалось как имя человека
    bot.register_next_step_handler(message, add_person_step)

def add_person_step(message):
    # Получаем имя человека из сообщения
    name = message.text.strip()

    # Создаем новый объект Person
    new_person = Person(name=name)
    
    # Добавляем объект в сессию
    session.add(new_person)
    
    # Сохраняем изменения в базе данных
    session.commit()

    # Отправляем пользователю сообщение о успешном добавлении человека
    bot.reply_to(message, f"Человек {name} успешно добавлен.")

def add_person_from_input(message):
    # Здесь можно отправить пользователю сообщение и ожидать ввода
    bot.reply_to(message, "Введите имя человека:")

    # После получения ответа от пользователя можно вызвать функцию add_person_from_input
    # и передать имя из сообщения, например:
    # name = message.text
    # add_person_from_input(name)


























































@bot.message_handler(commands=['eda'])
def eda(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item_calories = types.KeyboardButton('Добавить калории')
    item_water = types.KeyboardButton('Добавить воду')
    markup.add(item_calories, item_water)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

    # Получаем текущую дату
    today = datetime.now().date()

    # Получаем сумму калорий и воды за сегодня
    calories_today = session.query(func.sum(Nutrition.calorie_count)).filter(Nutrition.date >= today).scalar() or 0
    water_today = session.query(func.sum(Nutrition.water_quantity)).filter(Nutrition.date >= today).scalar() or 0

    # Отправляем результат пользователю
    bot.send_message(message.chat.id, f"Калории за сегодня: {calories_today} калорий")
    bot.send_message(message.chat.id, f"Вода за сегодня: {water_today} мл")

# Обработчик нажатия на кнопку "Добавить калории"
# Обработчик нажатия на кнопку "Добавить калории"
@bot.message_handler(func=lambda message: message.text == 'Добавить калории')
def add_calories(message):
    bot.reply_to(message, "Введите количество калорий:")
    bot.register_next_step_handler(message, process_calories_step)

def process_calories_step(message):
    try:
        calorie_count = int(message.text)
        new_nutrition = Nutrition(calorie_count=calorie_count, date=datetime.now())
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
        new_nutrition = Nutrition(water_quantity=water_quantity, date=datetime.now())
        session.add(new_nutrition)
        session.commit()
        bot.reply_to(message, 'Количество воды успешно добавлено в базу данных!')
    except ValueError:
        bot.reply_to(message, 'Пожалуйста, введите число.')










bot.infinity_polling()
