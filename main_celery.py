from celery_app import celery, app
from model.db import db

db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        celery.start()
