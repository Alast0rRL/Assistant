from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Создаем экземпляр Engine для подключения к базе данных SQLite
engine = create_engine('sqlite:///example.db', echo=True)  # echo=True для вывода выполненных SQL-запросов

# Создаем базовый класс моделей
Base = declarative_base()

# Определяем модель для таблицы "people"
class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Определяем связь "один-ко-многим" с таблицей "notes"
    notes = relationship("Note", back_populates="person")

# Определяем модель для таблицы "notes"



class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    person_id = Column(Integer, ForeignKey('people.id'))  # Внешний ключ, связывающий с таблицей "people"

    # Определяем связь "многие-ко-одному" с таблицей "people"
    person = relationship("Person", back_populates="notes")






class Nutrition(Base):
    __tablename__ = 'nutrition'

    id = Column(Integer, primary_key=True)
    date = Column(String)  # Можно использовать DateTime для даты и времени
    water_quantity = Column(Integer)
    calorie_count = Column(Integer)


















# Создаем таблицы в базе данных
Base.metadata.create_all(engine)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

