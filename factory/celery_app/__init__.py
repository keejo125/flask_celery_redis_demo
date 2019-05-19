# -*- coding: utf-8 -*-
from celery import Celery
from celery.schedules import crontab

celery = Celery('celery_app',
broker='redis://localhost:6379/1',
backend='redis://localhost:6379/1',
include=['celery_app.tasks','app.main.tasks', 'app.scheduled.tasks'],
)
celery.conf.update(
  CELERYBEAT_SCHEDULE = {
  'add-every-minute': {
      'task': 'app.scheduled.tasks.scheduled_task',
      'schedule': crontab(minute='*'),
      }
  },
  CELERY_TIMEZONE = 'Asia/Shanghai'
)
