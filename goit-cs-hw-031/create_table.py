import psycopg2  # бібліотека psycopg2, яка дозволяє Python підключатись до бази даних PostgreSQL та виконувати SQL-запити.

from dotenv import load_dotenv # завантажує змінні з .env у середовище
import os


# Параметри підключення (згідно з docker-compose.yml) взяті .env файла з метою приховання особистих даних користувача
load_dotenv()   # завантажує змінні з .env у середовище

db_config = {                           
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT"),
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD")
}

# SQL-запити
sql_query = """
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  fullname VARCHAR(100),
  email VARCHAR(100) UNIQUE
);

CREATE TABLE status (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE
);

CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  title VARCHAR(100),
  description TEXT,
  status_id INTEGER,
  user_id INTEGER,
  FOREIGN KEY (status_id) REFERENCES status(id),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

def create_tables(): 
    try:
        # Підключення до бази даних
        connection = psycopg2.connect(**db_config)   # Створює з'єднання з базою через psycopg2.connect(...).

        connection.autocommit = True    # Встановлює autocommit = True, щоб не потрібно було вручну викликати connection.commit(). 
        cursor = connection.cursor()    # Створює курсор (cursor) — об’єкт, через який можна виконувати SQL-запити.

        # Виконання SQL
        cursor.execute(sql_query)              # Курcор виконує SQL-запити з sql_query, які ми підготували раніше.
        print("Таблиці успішно створені.")

    except Exception as e:
        print("Помилка під час створення таблиць:", e)

    finally:
        if connection:            # Закриваємо підключення до бази даних — важливо, щоб не було "висячих" з'єднань.
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_tables()


##### Завдання 1.1 (аналог в python того, що зробили в DBeaver файлі sql_create_table.sql)

'''
Покрокова інструкція

1. Створіть таблиці у вашій PostgreSQL базі даних відповідно до вимог. Використовуйте належні типи даних та обмеження.

Вимоги до структури бази даних:


1.1. Таблиця users:

id: Первинний ключ, автоінкремент (тип SERIAL),
fullname: Повне ім'я користувача (тип VARCHAR(100)),
email: Електронна адреса користувача, яка повинна бути унікальною (тип VARCHAR(100)).


1.2. Таблиця status:

id: Первинний ключ, автоінкремент (тип SERIAL),
name: Назва статусу (тип VARCHAR(50)), повинна бути унікальною. Пропонуємо наступні типи [('new',), ('in progress',), ('completed',)].


1.3. Таблиця tasks:

id: Первинний ключ, автоінкремент (тип SERIAL),
title: Назва завдання (тип VARCHAR(100)),
description: Опис завдання (тип TEXT),
status_id: Зовнішній ключ, що вказує на id у таблиці status (тип INTEGER),
user_id: Зовнішній ключ, що вказує на id у таблиці users (тип INTEGER).


2. Переконайтеся, що поля email у таблиці users та name у таблиці status є унікальними.

3. Налаштуйте зв'язки між таблицями таким чином, щоб при видаленні користувача автоматично видалялися всі його завдання (каскадне видалення).

4. Напишіть скрипт створення цих таблиць.
'''


### Пояснення до коду
'''
🧠 Що таке транзакція у SQL?
У SQL будь-який запит, який змінює дані (наприклад, INSERT, UPDATE, DELETE, CREATE TABLE, DROP TABLE, і т.д.) виконується в межах транзакції.

🔁 Транзакція — це:
логічна група операцій, які виконуються як одне ціле (успішно або ні),
до моменту підтвердження (через COMMIT) — зміни не зберігаються остаточно.

🔧 Поведінка за замовчуванням у psycopg2
У бібліотеці psycopg2:

після connect(...) з'єднання автоматично створює транзакцію;
коли ти виконуєш cursor.execute(...), зміни відбуваються лише тимчасово;
щоб зберегти ці зміни в БД — потрібно виконати connection.commit() вручну.

❗Без commit():
створені таблиці не збережуться,
вставлені дані не збережуться,
для DDL (типу CREATE, DROP, ALTER) це особливо важливо.

✅ Що робить connection.autocommit = True?

Коли ти встановлюєш:
connection.autocommit = True
Це означає:

кожен запит одразу виконується і зберігається в БД без необхідності викликати commit();
psycopg2 не створює явну транзакцію, а відправляє кожен запит одразу в базу.

🟢 Коли це зручно?
autocommit = True зручно використовувати, коли:

Випадок	Пояснення
CREATE TABLE, DROP TABLE, ALTER TABLE	Це DDL-команди, які часто виконуються разово, без залежності між ними.
Скрипти ініціалізації	Ти просто хочеш швидко створити структуру БД.
Вставка початкових даних	Якщо не треба робити багато вставок у рамках однієї транзакції.


✅ Після запуску
Коли ти виконуєш цей файл (python create_table.py), він:

Підключається до PostgreSQL в контейнері через порт 5434.
Видаляє старі таблиці (якщо були).
Створює нові таблиці згідно з вимогами.
'''