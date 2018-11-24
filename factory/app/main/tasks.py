# -*- coding: utf-8 -*-
from celery_app import celery
import time
import random

@celery.task(bind=True)
def main_task(self, task_flag):
    print(task_flag + " app.main.task start")
    delay_time = random.randint(5, 20)
    print(delay_time)
    for i in range(delay_time):
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': delay_time,
                                'status': "sleeping"})
        print(i)
        time.sleep(1)
    print(task_flag + " app.main.task end")
    return {'current': 100, 'total': 100, 'status': 'awake!',
            'result': "done!"}
