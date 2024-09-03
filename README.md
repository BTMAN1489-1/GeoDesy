# GeoDesy corp.
## От автора

Здесь будет дана краткая инструкция, которая должна помочь всем обделенным и нуждающимся запустить данный проект.
Автор надеется, что читатель уже далеко не профан в искусстве программирования, поэтому некоторые детали будут - с Вашего позволения, конечно, - опущены.
Сие действие представимо в трех актах. Начнем-с.

## Прелюдия
### _Настройка окружения проекта_
- Создайте и настройте почтовый ящик для рассылки писем. Инструкцию можно найти, например, [здесь](https://yandex.ru/support/mail/mail-clients/others.html)
- Установите [СУБД PostgreSQL](https://postgrespro.ru/docs/postgresql/16/tutorial), создайте базу данных, настройте подключение
- Установите [Python](https://www.python.org/downloads/release/python-3125/) версии &#8805; 3.11
- Установите и настройте утилиту [GNU/make](https://www.gnu.org/software/make/)
- Клонируйте данный репозиторий (если Вы это ещё почему-то не сделали)
- Согласно образцу заполните файл `env.dist`

### _Замечание к установке Python_

Если Вы счаcтливый обладатель...

#### _Windows_

- Просто [скачайте](https://www.python.org/downloads/release/python-3125/) и запустите установщик
- Добавьте путь к бинарнику `python.exe` в переменную среды `Path`

#### _Linux_

- Соберите проект из исходников с [официального сайта](https://www.python.org/downloads/release/python-3125/)

    Или же...

- `sudo apt install python3.11`
- `sudo apt install python3.11-venv`

### _Замечание к установке GNU/make_
#### _Windows_

- Просто [скачайте](https://gnuwin32.sourceforge.net/packages/make.htm) и запустите установщик
- Добавьте путь к бинарнику `make.exe` в переменную среды `Path`

#### _Linux_
- `sudo apt install make`

### _Замечание к заполнению `env.dist` файла_
#### _Настройка почтовой рассылки_
```properties
# Адрес эл. почты для рассылки писем 
EMAIL_USER=some_email@yandex.ru

# Пароль от эл. почты или пароль приложения (как у Яндекса, например)
EMAIL_PASSWORD=qwerty

# Хост и порт SMTP-сервера для рассылки сообщений
EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=465
```

#### _Настройка безопасности_
```properties
# Секретный ключ используется для шифрования и эл. подписи. 
# Секретный ключ должен быть криптографически стойким и иметь максимальную длину в 64 байта
# Для генерации секрета можно использовать встроенный в python модуль secrets
SECRET_KEY=some-secret-key

# Список разрешенных доменных имен и IP-адресов (через запятую, без пробелов)
ALLOWED_HOSTS=localhost,127.0.0.1,somesite.ru

# Списки разрешенных источников для CORS и CSRF -политики (через запятую, без пробелов)
CORS_ALLOWED_ORIGINS=http://somesite.ru,https://somesite.ru,https://somesite.ru:8080
CSRF_TRUSTED_ORIGINS=http://somesite.ru,https://somesite.ru,https://somesite.ru:8080
```

#### _Настройка БД_
```properties
# Адрес и порт сервера СУБД
PGHOST=localhost
PGPORT=5432

# Имя базы данных, которое было указано при создании
PGDATABASE=geodesy_db

# Имя и пароль владельца базы данных 
PGUSER=postgres
PGPASSWORD=12345
```

#### _Настройка суперпользователя_
```properties
# Пароль и E-mail суперпользователя, которые могут использоваться для авторизации в админ-панели
DJANGO_SUPERUSER_EMAIL=superuser@gmail.com
DJANGO_SUPERUSER_PASSWORD=hard-password
```
## Акт &#8544;
Для настройки проекта необходимо зайти в папку проекта и выполнить команду...
#### _Windows_
```shell
make -f Makefile.win setup
```

#### _Linux_
```shell
make setup
```

...и дождаться завершения настройки (необходимо Интернет-соединение).

## Акт &#8545;
В случае успеха можно поднять сервер камандой...
#### _Windows_
```shell
make -f Makefile.win start server-host=127.0.0.1 server-port=8000
```

#### _Linux_
```shell
make start server-host=127.0.0.1 server-port=8000
```
...где параметры `server-host`, `server-port` необязательны и равны по умолчанию `127.0.0.1` и `8000`, соответственно.
## Акт &#8546;

После запуска сервера можно ознакомиться с документацией API по маршруту:

- `/api/schema/redoc/` (просто документация)
- `/api/schema/swagger-ui/` (интерактивная документация)

Или же зайти в админ-панель по маршруту `/admin/`


## Постлюдия

Рассмотрим подробнее использование утилиты GNU/make в данном проекте.

Синтаксис для...
#### _Windows_
```shell
make -f Makefile.win [command] [paramet1] [paramet2] ...
```

#### _Linux_
```shell
make [command] [paramet1] [paramet2] ...
```

### _Команды_
#### env-prepare
```shell
# Создает файл .env на основе файла env.dist
make env-prepare
```

#### create-venv
```shell
# Создает виртуальное окружение в текущей директории
make create-venv
```

#### install-requirements
```shell
# Создает виртуальное окружение и загружает туда все зависимости
make install-requirements
```

#### db-prepare
```shell
# Подготавливает базу данных к использованию (повторный вызов может привезти к ошибке)
make db-prepare
```

#### db-make-migrations
```shell
# Создает файлы миграции БД
make db-make-migrations
```

#### db-migrate \[app-name] \[migration-name]:
```shell
# Применяет миграцию БД с определенным номером (migration-name) для определенного приложения (app-name)
make db-migrate app-name=some_app migration-name=0001
```

#### create-superuser
```shell
# Создает суперпользователя
make create-superuser
```

#### setup
```shell
# Запускает настройку проекта.
# Эквивалентно последовательному выполнению команд install-requirements, env-prepare, db-prepare, create-superuser
make setup
```

#### start \[server-host] \[server-port]:
```shell
# Запускает сервер с указанными хостом и портом
make start server-host=127.0.0.1 server-port=8000
```

