# GeoDesy corp.
## Прелюдия

Здесь будет дана краткая инструкция, которая должна помочь всем обделенным и нуждающимся запустить данный проект.
Автор надеется, что читатель уже далеко не профан в искусстве программирования, поэтому некоторые детали будут - с Вашего позволения, конечно, - опущены.
Сие действие представимо в трех актах. Начнем-с.

## Акт &#8544;
### _Настройка окружения проекта_
- Создайте почтовый ящик для рассылки писем. Инструкцию можно найти, например, [здесь](https://yandex.ru/support/mail/mail-clients/others.html)
- [Установите и настройте СУБД](https://postgrespro.ru/docs/postgresql/16/tutorial)
- Зайдите в папку проекта
- Создайте файл `.env` и наполните его смыслом, исходя из шаблона `.env.dist`
- Установите все зависимости командой `pip install -r requirements.txt`

## Акт &#8545;
### _Настройка базы данных_

- Для начала выполните скрипт `db_queries/MigrateFederalDistricts.sql`
- Затем - скрипт `db_queries/MigrateFederalSubjects.sql`
- Зайдите в папку `GeoDesy/`
- Создайте файлы миграции командой `python manage.py makemigrations`
- Выполните миграции командой `python manage.py migrate`

## Акт &#8546;
### _Окончательня настройка и запуск проекта_

- Создайте супер пользователя командой `python manage.py createsuperuser` (Необязательно)
- Запустите проект, выполнив команду `python manage.py runserver`

Готово!

## Постлюдия

С документацией API можно ознакомиться по адресу `http://<your_damain>/api/schema/redoc/`.
Интерактивная дукументация доступна по ссылке `http://<your_damain>/api/schema/swagger-ui/`.
> Освоение документации - тяжкий труд, зачастую неблагадарный. Желаю Вам успеха в этом нелегком деле.
BTMAN1489-1 (неизвестно - 2024 год)
