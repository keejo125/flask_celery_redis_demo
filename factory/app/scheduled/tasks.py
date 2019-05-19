# -*- coding: utf-8 -*-
from celery_app import celery
import time


@celery.task
def scheduled_task(*args, **kwargs):
    print(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())))
