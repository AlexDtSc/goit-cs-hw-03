DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS users;

----- 1.1 Таблиця users

CREATE TABLE users 
(
 id SERIAL primary key,
 fullname VARCHAR(100),
 email VARCHAR(100) UNIQUE
);


----- 1.2 Таблиця status

CREATE TABLE status 
(
 id SERIAL primary key,
 name VARCHAR(50) unique
);

----- 1.3 Таблиця tasks

CREATE table tasks
(
 id SERIAL primary key,
 title VARCHAR(100),
 description TEXT,
 status_id INTEGER, 
 user_id INTEGER,
 foreign key (status_id) REFERENCES status (id),
 foreign key (user_id) references users (id)
   on delete cascade
)
 
 /* 
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
  */
