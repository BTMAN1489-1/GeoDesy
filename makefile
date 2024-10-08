python-venv = ./venv/bin/python3
server-host = 127.0.0.1
server-port = 8000
env-prepare:
	cp -n env.dist .env

install-requirements: create-venv
	 $(python-venv) -m pip install --upgrade pip
	 $(python-venv) -m pip install -r requirements.txt

create-venv:
	python3 -m venv ./venv

db-prepare:
	$(python-venv) ./GeoDesy/manage.py migrate

db-make-migrations:
	$(python-venv) ./GeoDesy/manage.py makemigrations

db-migrate:
	$(python-venv) ./GeoDesy/manage.py migrate $(app-name) $(migration-name)

create-superuser:
	$(python-venv) ./GeoDesy/manage.py createsuperuser --no-input

start:
	$(python-venv) ./GeoDesy/manage.py runserver $(server-host):$(server-port)

setup: install-requirements env-prepare db-prepare create-superuser
