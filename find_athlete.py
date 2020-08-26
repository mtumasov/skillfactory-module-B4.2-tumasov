# испортируем модули стандартнй библиотеки uuid и datetime
import uuid
import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из нее
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# для проверки правильности ввода даты
from datetime import datetime, date, time
# from datetime import datetime

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.INTEGER, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пренадлежность Male / Female
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # дата рождения
    birthdate = sa.Column(sa.Text)
    # рост
    height = sa.Column(sa.REAL)


# Класс для таблицы с атлетами
class Athelete(Base):
    # Название таблицы
    __tablename__ = "athelete"
    # Идентификатор атлета
    id = sa.Column(sa.Integer, primary_key=True)
    # Дата рождения
    birthdate = sa.Column(sa.Text)
    # Рост атлета
    height = sa.Column(sa.REAL)
    # Имя атлета
    name = sa.Column(sa.Text)


# Функция, которая создаёт сессию для подключения к ДБ
def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


# Функция, которая ищет пользователя с заданным ID
def find_user(user_id):
    # Создадим сессию
    session = connect_db()
    # Сделаем запрос
    user = session.query(User).filter(User.id == user_id).first()
    # Закроем сессию
    session.close()
    # Возращаем пользователя
    return user


# Функция, которая принимает как аргумент рост юзера
# Возвращает атлета с минимальной разницей в росте с юзером
def find_by_height(user_height):
    # Создадим сессию
    session = connect_db()

    # Теперь возьмём всех атлетов из БД
    # У некоторых атлетов стоит None в поле height
    # Поэтому отфильтруем, что высота положительная
    # Получили список с атлетами
    atheletes = session.query(Athelete).filter(Athelete.height > 0).all()

    # Закроем сессию
    session.close()

    # Теперь найдем атлета с минимальной разницей в росте
    # Переменная candidate - это атлет-кандидат
    # У кандидата минимальная разница в росте с юзером
    # Пусть сначала кандидатом будет первый атлет
    candidate = atheletes[0]

    # В цикле пройдем по атлетам
    for athelete in atheletes:
        # Посчитаем разницу роста кандидата и юзера
        candidate_diff = abs(candidate.height - user_height)  # Что это abs?
        # Теперь посчитаем разницу роста для текущего атлета и юзера
        athelete_diff = abs(athelete.height - user_height)

        # Если у текущего атлета разница в росте меньше чем у кандидата
        if athelete_diff < candidate_diff:
            # То теперь этот атлет и есть новый кандидат
            candidate = athelete
        return candidate


# Функция,  возвращает разность дат
# date_1, date_2 - строки с датами
def date_diff(date_1, date_2):
    # Преобразуем строку date_1 с помощью знакомой вам функции
    # В объект datetime
    datetime_1 = datetime.strptime(date_1, "%Y-%m-%d")
    # Аналогично для второй даты
    datetime_2 = datetime.strptime(date_2, "%Y-%m-%d")
    # Считаем модуль разности дат
    diff = abs(datetime_1 - datetime_2)
    # Возращаем разность
    return diff


#Функция принмает дату  и возвращает ближайшую
def find_by_birthdate(user_birthdate):
    # Создадим сессию
    session = connect_db()
    atheletes1 = session.query(Athelete).all()
    # Закроем сессию
    session.close()
    candidate1 = atheletes1[0]

    for athelete1 in atheletes1:
        candidate_diff = date_diff(candidate1.birthdate, user_birthdate)
        athelete_diff = date_diff(athelete1.birthdate, user_birthdate)
        if athelete_diff < candidate_diff:
            candidate1 = athelete1

    return candidate1


def main():
    # Для начала запросим ID пользователя
    user_id = int(input("Введите ID пользователя: "))

    # Находим юзера по ID
    user = find_user(user_id)

    # Запрос либо вернет объект класса User, если пользователь с таким ID есть в БД
    # Либо вернет None, если такого пользователя нет
    # Поэтому условие выполняется, когда пользователь найден
    if user:
        # Вызовем фукнцию, чтобы найти атлета с минимальной разницей по росту
        athelete_close_height = find_by_height(user.height)
        # Выведем результат
        print("Ближайший по росту атлет: {} {}".format(
            athelete_close_height.name, athelete_close_height.height))
        # Вызовем фукнцию, чтобы найти атлета с минимальной разницей по дате рождения
        athelete_close_birthdate = find_by_birthdate(user.birthdate)
        # Выведем результат
        print("Ближайший по возрасту атлет: {} {}".format(
            athelete_close_birthdate.name, athelete_close_birthdate.birthdate))

    else:
        print("Пользователь с таким ID не найден")


if __name__ == "__main__":
    main()