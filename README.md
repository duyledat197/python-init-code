 # Backend API Web Service

## Documentation
Postman collection: https://documenter.getpostman.com/view/5341276/S1LwzTNg?version=latest

## Prerequisites

* Python 3.7
* Postgres

Development Tool:

* `pip8`: Python formatter

## Development Setup

1. Install dependencies:
```
pip install requirements.txt
```

2. Setup `.env` file
```
virtualenv -p `which python3` .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Setup database

```
postgresql
```

4. (Optional) access Postgres database
```
psql "postgresql://:@localhost:5432/<db_name>"
```

5. Set up redis



6. (Optional) access Redis database
```
redis-cli -h 127.0.0.1 -p 6379 -n 0
```

7. Start Celery worker:
```
python main_celery.py worker --loglevel=info -Ofair --beat
```

8. Start project
```
python main.py
```

## Deploy server

Run with docker

1. Setup docker
- install docker
- install docker-compose
- install make

2. Start project
```
make deploy-server
```

3. Set config to database
```
docker exec -it <docker container api> python manage.py seed_all
```
