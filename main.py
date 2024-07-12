from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os

app = Flask(__name__)

# Настройка базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для хранения данных о воде и калориях
class Tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор
    total_water = db.Column(db.Integer, default=0)  # Общее количество выпитой воды
    total_calories = db.Column(db.Integer, default=0)  # Общее количество потребленных калорий
    date = db.Column(db.Date, default=datetime.now(timezone.utc).date)  # Дата записи

# Модель для хранения истории
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор
    date = db.Column(db.Date, default=datetime.now(timezone.utc).date)  # Дата записи
    total_water = db.Column(db.Integer, default=0)  # Общее количество выпитой воды
    total_calories = db.Column(db.Integer, default=0)  # Общее количество потребленных калорий

# Создаем базу данных и начальную запись, если это необходимо
with app.app_context():
    db.create_all()  # Создает таблицы, если они не существуют
    if Tracker.query.count() == 0:  # Проверка, есть ли записи в таблице Tracker
        db.session.add(Tracker())  # Добавление начальной записи
        db.session.commit()  # Подтверждение изменений

# Функция для сброса трекера и сохранения данных в историю, если дата изменилась
def reset_tracker():
    today = datetime.now(timezone.utc).date()  # Текущая дата
    tracker = Tracker.query.first()  # Получение первой записи из таблицы Tracker
    if tracker.date != today:  # Проверка, изменилась ли дата
        # Создание новой записи в истории с текущими данными
        history_entry = History(date=tracker.date, total_water=tracker.total_water, total_calories=tracker.total_calories)
        db.session.add(history_entry)  # Добавление записи в историю
        tracker.total_water = 0  # Сброс количества воды
        tracker.total_calories = 0  # Сброс количества калорий
        tracker.date = today  # Обновление даты в трекере
        db.session.commit()  # Подтверждение изменений

@app.route('/', methods=['GET', 'POST'])
def index():
    reset_tracker()  # Сброс трекера при каждом запросе на главную страницу
    tracker = Tracker.query.first()  # Получение текущей записи трекера
    calculated_calories = ""  # Переменная для хранения рассчитанных калорий
    if request.method == 'POST':  # Обработка POST-запросов
        if 'add_water' in request.form:  # Добавление воды
            water_amount = int(request.form['water_amount'])
            tracker.total_water += water_amount
        elif 'preset_water' in request.form:  # Добавление предустановленного количества воды
            water_amount = int(request.form['preset_water'])
            tracker.total_water += water_amount
        elif 'add_calories' in request.form:  # Добавление калорий
            calories_amount = int(request.form['calories_amount'])
            tracker.total_calories += calories_amount
        elif 'reset' in request.form:  # Сброс данных
            tracker.total_water = 0
            tracker.total_calories = 0
        elif 'calculate_calories' in request.form:  # Расчет калорий
            calories_per_100g = int(request.form['calories_per_100g'])
            weight = int(request.form['weight'])
            calculated_calories = (calories_per_100g / 100) * weight  # Расчет общего количества калорий
        db.session.commit()  # Подтверждение изменений в базе данных
        return redirect(url_for('index'))  # Перенаправление на главную страницу для обновления данных
    return render_template('index.html', total_water=tracker.total_water, total_calories=tracker.total_calories, calculated_calories=calculated_calories)

@app.route('/history')
def history():
    history_records = History.query.order_by(History.date.desc()).all()  # Получение всех записей из истории, отсортированных по дате
    return render_template('history.html', history_records=history_records)

@app.route('/edit/<int:history_id>', methods=['GET', 'POST'])
def edit_history(history_id):
    record = History.query.get_or_404(history_id)  # Получение записи или 404 ошибка, если запись не найдена
    if request.method == 'POST':
        record.total_water = int(request.form['total_water'])
        record.total_calories = int(request.form['total_calories'])
        db.session.commit()  # Подтверждение изменений в базе данных
        return redirect(url_for('history'))  # Перенаправление на страницу истории
    return render_template('edit_history.html', record=record)

@app.errorhandler(Exception)
def handle_exception(e):
    return render_template('error.html', error=str(e)), 500  # Обработка ошибок и отображение страницы ошибки

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Запуск приложения Flask
