from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure
from bson.objectid import ObjectId

# Підключення до MongoDB
try:
    client = MongoClient("mongodb://localhost:27018/")
    db = client["cat_database"]
    collection = db["cats"]
    # Перевірка з'єднання
    client.admin.command('ping')
    print("MongoDB підключено успішно")
except ConnectionFailure:
    print("Не вдалося підключитися до MongoDB, перевірте з'єднання")


def create_document():
    try:
        name = input("Введіть ім'я кота: ")
        age = int(input("Введіть вік кота: "))
        features = input("Введіть характеристики через кому: ").split(',')

        doc = {
            "name": name.strip(),
            "age": age,
            "features": [f.strip() for f in features]
        }

        result = collection.insert_one(doc)
        print(f"Документ створено з _id: {result.inserted_id}")
    except PyMongoError as e:
        print(f"Помилка при роботі з MongoDB: {e}")
    except ValueError as e:
        print(f"Помилка введення: {e}")


def read_all_documents():
    try:
        documents = collection.find()
        for doc in documents:
            print(doc)
    except PyMongoError as e:
        print(f"Помилка читання: {e}")


def read_document_by_name():
    try:
        name = input("Введіть ім'я кота для пошуку: ")
        doc = collection.find_one({"name": name})
        if doc:
            print(doc)
        else:
            print("Кота з таким ім'ям не знайдено.")
    except PyMongoError as e:
        print(f"Помилка читання: {e}")


def update_document_age():
    try:
        name = input("Введіть ім'я кота для оновлення віку: ")
        new_age = int(input("Введіть новий вік: "))
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count:
            print("Вік оновлено.")
        else:
            print("Кота не знайдено або вік не змінено.")
    except (PyMongoError, ValueError) as e:
        print(f"Помилка оновлення: {e}")


def add_feature_to_document():
    try:
        name = input("Введіть ім'я кота для додавання характеристики: ")
        feature = input("Введіть нову характеристику: ")
        result = collection.update_one({"name": name}, {"$push": {"features": feature}})
        if result.modified_count:
            print("Характеристику додано.")
        else:
            print("Кота не знайдено або характеристика вже існує.")
    except PyMongoError as e:
        print(f"Помилка додавання: {e}")


def delete_document():
    try:
        name = input("Введіть ім'я кота для видалення: ")
        result = collection.delete_one({"name": name})
        if result.deleted_count:
            print("Кота видалено.")
        else:
            print("Кота не знайдено.")
    except PyMongoError as e:
        print(f"Помилка видалення: {e}")


def delete_all_documents():
    try:
        confirm = input("Ви впевнені, що хочете видалити ВСІ записи? (yes/no): ")
        if confirm.lower() == "yes":
            result = collection.delete_many({})
            print(f"Видалено {result.deleted_count} документ(ів).")
        else:
            print("Операцію скасовано.")
    except PyMongoError as e:
        print(f"Помилка масового видалення: {e}")


def main():
    while True:
        print("\nДоступні дії:")
        print("1 - Створити запис про тварину")
        print("2 - Показати всі записи")
        print("3 - Пошук запису за ім'ям тварини")
        print("4 - Оновити вік тварини")
        print("5 - Додати особливість до тварини")
        print("6 - Видалити запис про тварину")
        print("7 - Видалити всі записи")
        print("8 - Вийти")
        choice = input("Виберіть дію: ")

        if choice == "1":
            create_document()
        elif choice == "2":
            read_all_documents()
        elif choice == "3":
            read_document_by_name()
        elif choice == "4":
            update_document_age()
        elif choice == "5":
            add_feature_to_document()
        elif choice == "6":
            delete_document()
        elif choice == "7":
            delete_all_documents()
        elif choice == "8":
            print("Вихід...")
            break
        else:
            print("Некоректний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
