from faker import Faker
import psycopg2
import random

from dotenv import load_dotenv # завантажує змінні з .env у середовище
import os


# Налаштування Faker
fake = Faker()


# Параметри підключення (згідно з docker-compose.yml) взяті .env файла з метою приховання особистих даних користувача
load_dotenv()   # завантажує змінні з .env у середовище

# Конфігурація підключення до бази даних (замінити на реальні параметри при використанні. # Параметри підключення (згідно з docker-compose.yml)
db_config = {
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT"),
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD")
}

# Функції для генерації даних
def generate_users(n=10):
    ''' Генерує випадкові дані для таблиці користувачів '''
    users = []
    for _ in range(n):
        users.append( (fake.name(), fake.email()))
    return users


def generate_statuses():
    ''' Генерує фіксовані статуси для таблиці статусів '''
    statuses = [('new',), ('in progress',), ('completed',)]
    return statuses

def generate_tasks(n=30, user_count=10, status_count=3):
    ''' Генерує випадкові дані для таблиці завдань '''
    tasks = []
    for _ in range(n):
        title = fake.sentence(nb_words=4)
        description = fake.paragraph(nb_sentences=3)
        status_id = random.randint(1, status_count)
        user_id = random.randint(1, user_count)
        tasks.append((title, description, status_id, user_id))
    return tasks


# Функція для заповення бази даних
def populate_database():
    conn = None
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Вставка користувачів
        users = generate_users()
        cur.executemany("INSERT INTO users (fullname, email) VALUES (%s, %s)", users)

        # Вставка статусів
        statuses = generate_statuses()
        cur.executemany("INSERT INTO status (name) VALUES (%s)", statuses)

        # Вставка завдань
        tasks = generate_tasks()
        cur.executemany("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)", tasks)

        conn.commit()  # зберігаємо введені дані в таблиці (проводимо транзакцію)
        cur.close()
        print('Дані додано в таблицю успішно')
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':

    # Виклик функції для заповення бази даних
    populate_database()