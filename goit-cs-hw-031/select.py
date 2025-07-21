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

sql_file_path = 'sql_selects.sql'

def run_all_queries():
    connection = None
    cursor = None
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        queries = [q.strip() for q in sql_content.split(';') if q.strip()]  # розбиває 1 рядок із запитами по розділювачу ; на список із 14 рядків із запитами, щоб можна було результат кожного запиту виводити окремо в консоль

        connection = psycopg2.connect(**db_config)          # Створює з'єднання з базою через psycopg2.connect(...).
        connection.autocommit = True                        # Встановлює autocommit = True, щоб не потрібно було вручну викликати connection.commit().
        cursor = connection.cursor()                        # Створює курсор (cursor) — об’єкт, через який можна виконувати SQL-запити.

        for i, query in enumerate(queries, start=1):
            print(f"\n--- Результат запиту #{i} ---")
            try:
                cursor.execute(query)                        # Курcор виконує SQL-запити з sql_query, які ми підготували раніше.
                if 'select' in query.lower():
                    rows = cursor.fetchall()
                    if not rows:
                        print("Немає результатів")
                    else:
                        for row in rows:
                            print(row)
                else:
                    print("Запит виконано (не SELECT)")
            except Exception as qerr:
                print(f"Помилка у запиті #{i}:\n{qerr}")

    except Exception as e:
        print("Загальна помилка:", e)

    finally:
        if cursor:
            cursor.close()
        if connection:           # Закриваємо підключення до бази даних — важливо, щоб не було "висячих" з'єднань.
            connection.close()
            
if __name__ == "__main__":
    run_all_queries()
