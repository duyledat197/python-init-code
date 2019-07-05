import os

from celery import Celery
from celery.schedules import crontab


def make_celery(app):
    celery = Celery(
        'tasks',
        broker=os.environ.get('CELERY_BROKER_URL'),
        backend=os.environ.get('CELERY_RESULT_BACKEND'),
        imports=(),
        include=[
            'tasks.mail',
        ]
    )
    celery.conf.update(app.config)
    celery.conf.timezone = os.environ.get('CELERY_TIMEZONE')
    celery.conf.beat_schedule = {
        'schedule_categories_endings': {
            'task': 'tasks.category.schedule_categories_endings',
            'schedule': crontab(hour=18, minute=16),
            'args': (),
        },
        'schedule_categories_removed_events': {
            'task': 'tasks.category.schedule_categories_removed_events',
            'schedule': crontab(hour=18, minute=16),
            'args': (),
        },
    }

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
