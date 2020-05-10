import re
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from find_athlete import find

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()
class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Date)
    height = sa.Column(sa.Float)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def request_data():
    print("Создание нового пользователя, введите следующие данные:")
    first_name = check_in("Имя:").capitalize()
    last_name = check_in("Фамилия:").capitalize()
    email = check_in("Email:", r'[a-zA-Z0-9.]+@\w+(\.\w+)+')
    gender = check_in("Пол ('М' либо 'Ж'):", r'[МмЖж]').lower()
    height = check_in("Рост, см (округлить до целого):", r'\d+')
    birthdate = datetime.datetime.strptime(check_in("Дата рождения в виде число.месяц.год (пример 30.12.2019):", r'\d\d\.\d\d\.\d{4}'), '%d.%m.%Y').date()
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        gender=gender,
        height=int(height)/100,
        birthdate=birthdate
    )
    return user

# простенькая проверка на коррестность вводимых данных
def check_in(request, expression='\w+'):
    while True:
        strng = input(request)
        if re.match(expression, strng): break
        else: print('Введены некорректные данные, еще попытка: ')
    return strng

def main():
    session = connect_db()
    while True:
        mode = input("Выберите режим.\n1 - найти пользователя по id\n2 - ввести данные нового пользователя\n3 - выход\n")
        if mode == "1":
            user_id = input("Введите id пользователя для поиска: ")
            ath_heights, ath_birthdate = find(user_id, session, User)
            # атлеты выводятся по одному на запрос, но циклы нужны на случай, если мы захотим выводить полный список
            if ath_heights:
                for row in ath_heights:
                    print("Атлет близкий по росту, первый в списке: {} с ростом {} см".format(row['name'], int(row['height'] * 100)))
            if ath_birthdate:
                for row in ath_birthdate:
                    print("Атлет близкий по дате рождения, первый в списке: {}, родившийся {}".format(row['name'], row['birthdate']))
        elif mode == "2":
            user = request_data()
            session.add(user)
            session.flush()
            print("Ваш id в базе данных: ", user.id)
            session.commit()
            print("Спасибо, данные сохранены!")
        elif mode == '3':
            break
        else: print("Некорректный режим")
    print('Пока!')
if __name__ == "__main__":
    main()