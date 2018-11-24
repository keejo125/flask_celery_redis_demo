# -*- coding: utf-8 -*-
from celery import Celery

celery = Celery('celery_app',
broker='redis://localhost:6379/1',
backend='redis://localhost:6379/1',
include=['celery_app.tasks','app.main.tasks'])