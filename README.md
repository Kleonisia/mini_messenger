# mini_messenger
## Описание и инструкция по пользованию
**mini_messenger** представляет из себя своего рода *Discord* (*discord-lite* если хотите). После прохождение простой регистрации или входа в аккаунт(если он у вас уже есть) будет доступна возможность создать новую комнату и посмотреть список уже существующих комнат. Комната представляет собой чат в которой может писать каждый зарегистрировавшийся. Таким образом в новой комнате вы можете общаться с более чем одним человеком.
## Замечания
**mini_messenger** работает локально, поэтому для его тестирования необходимо запустить **_localhost_** в разных браузерах(или перейти по ссылке в разных браузерах) и войти (если уже есть аккаунты) или зарегистрироваться от разных аккаунтов. Вначале база данных *db.sqlite3* пуста, поэтому необходимо зарегистрировать несколько аккаунтов.
## Инструкция по работе
1. Склонируйте репозиторий себе на компьютер.
2. Запустите файл app.py (например, пропишите в терминал команду находясь в директории где находится файл app.py: *python3 app.py*)
## Разное
1. Использование БД
До создания аккаунта на сайте
![Check](/images/1.png)
Создали тестовый аккаунт с именем пользователя test
![Check](/images/2.png)
Создали тестовую комнату с названием test1
![Check](/images/3.png)
Написал пару тестовых сообщений
![Check](/images/4.png)
Результат хранения в БД
![Check](/images/5.png)
2. Примеры работы
Сообщения в тестовой комнате room1 в разных браузерах(по понятным причинам) с разных тестовых аккаунтах
![Check](/images/6.png)
![Check](/images/7.png)
![Check](/images/8.png)