from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для хранения данных о воде и калориях
class Tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_water = db.Column(db.Integer, default=0)
    total_calories = db.Column(db.Integer, default=0)
    date = db.Column(db.Date, default=datetime.now(timezone.utc).date)

# Модель для хранения истории
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.now(timezone.utc).date)
    total_water = db.Column(db.Integer, default=0)
    total_calories = db.Column(db.Integer, default=0)

# Создаем базу данных
with app.app_context():
    db.create_all()
    if Tracker.query.count() == 0:
        db.session.add(Tracker())
        db.session.commit()

def reset_tracker():
    today = datetime.now(timezone.utc).date()
    tracker = Tracker.query.first()
    if tracker.date != today:
        history_entry = History(date=tracker.date, total_water=tracker.total_water, total_calories=tracker.total_calories)
        db.session.add(history_entry)
        tracker.total_water = 0
        tracker.total_calories = 0
        tracker.date = today
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    reset_tracker()
    tracker = Tracker.query.first()
    if request.method == 'POST':
        if 'add_water' in request.form:
            water_amount = int(request.form['water_amount'])
            tracker.total_water += water_amount
        elif 'preset_water' in request.form:
            water_amount = int(request.form['preset_water'])
            tracker.total_water += water_amount
        elif 'add_calories' in request.form:
            calories_amount = int(request.form['calories_amount'])
            tracker.total_calories += calories_amount
        elif 'reset' in request.form:
            tracker.total_water = 0
            tracker.total_calories = 0
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', total_water=tracker.total_water, total_calories=tracker.total_calories)

@app.route('/history')
def history():
    history_records = History.query.order_by(History.date.desc()).all()
    return render_template('history.html', history_records=history_records)

@app.errorhandler(Exception)
def handle_exception(e):
    return render_template('error.html', error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
