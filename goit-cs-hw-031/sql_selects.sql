--Запити для виконання:
--
--1.  Отримати всі завдання певного користувача. 
-- Використайте SELECT для отримання завдань конкретного користувача за його user_id.
select t.title 
from tasks t 
where user_id = 1;


--2.  Вибрати завдання за певним статусом. 
--Використайте підзапит для вибору завдань з конкретним статусом, наприклад, 'new'.
select * 
from tasks t 
where t.status_id in 
      (
       select s.id
       from status s 
       where s.name = 'new'
      );

     
--3.  Оновити статус конкретного завдання. 
-- Змініть статус конкретного завдання на 'in progress' або інший статус.
update tasks  
SET status_id = 
   (
   select id 
   from status 
   where name = 'in progress'
   )
where id = 1;


--4.  Отримати список користувачів, які не мають жодного завдання. 
-- Використайте комбінацію SELECT, WHERE NOT IN і підзапит.
select u.fullname 
from users u 
where u.id not in 
   (
   select t.user_id
   from tasks t 
   );


--5.  Додати нове завдання для конкретного користувача. 
--Використайте INSERT для додавання нового завдання.
INSERT INTO tasks (title, description, status_id, user_id) VALUES ('Brush my teeth', 'Spill some water at toothbrush and put some toothpasta', 1, 1);



--6.  Отримати всі завдання, які ще не завершено. 
-- Виберіть завдання, чий статус не є 'завершено'.
select t.title 
from tasks t
where t.status_id not in 
   (
   select s.id
   from status s
   where s.name = 'completed'
   );


--7.  Видалити конкретне завдання. 
--Використайте DELETE для видалення завдання за його id.
delete from tasks t where t.id = 31;


--8.  Знайти користувачів з певною електронною поштою. 
-- Використайте SELECT із умовою LIKE для фільтрації за електронною поштою.
select u.fullname 
from users u 
where u.email like '%aige%';


--9.  Оновити ім'я користувача. 
--Змініть ім'я користувача за допомогою UPDATE.
update users set fullname = 'Pedro Pe' where id = 8;


--10. Отримати кількість завдань для кожного статусу. 
--Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами.
select s.name, count(t.id) as number_of_tasks
from status s 
join tasks t 
on s.id = t.status_id
group by s.name;


--11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти. 
-- Використайте SELECT з умовою LIKE в поєднанні з JOIN, щоб вибрати завдання, призначені користувачам, 
-- чия електронна пошта містить певний домен (наприклад, '%@example.com').
select t.title
from tasks t
join users u
on u.id = t.user_id 
where u.email like '%@example.net';


--12. Отримати список завдань, що не мають опису. 
--Виберіть завдання, у яких відсутній опис.
select t.title 
from tasks t 
where t.description is null or t.description ='';


--13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'. 
--Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом.
select u.fullname, t.title
from users u 
join tasks t 
on u.id = t.user_id 
join status s 
on s.id = t.status_id 
where s.name in ('in progress');


--14. Отримати користувачів та кількість їхніх завдань. 
--Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань.
select u.fullname, count(t.id) as number_of_tasks
from users u 
left join tasks t
on u.id = t.user_id
group by u.id, u.fullname
order by number_of_tasks desc
