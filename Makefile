.PHONY: test

run-dev:
	python main.py

test:
	PYTHONPATH=.:src pytest --disable-pytest-warnings --capture=no

run-celery:
	python main_celery.py worker --loglevel=info --beat

run-server:
	python manage.py db upgrade
	gunicorn --bind 0.0.0.0:5000 --workers 8 --threads 8 --pythonpath src 'main:create_app()'

deploy-server:
	git pull
	docker-compose down
	docker-compose up -d --build
