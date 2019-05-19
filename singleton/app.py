# -*- coding: utf-8 -*-
from flask import Flask, jsonify, url_for
from celery import Celery
from celery.schedules import crontab
import time
import random


app = Flask(__name__)
# 单独配置方式
# app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/0"
# app.config['CELERY_RESULT_BACKEND'] = "redis://localhost:6379/0"
# 批量配置方式
app.config.update(
    CELERY_BROKER_URL = "redis://localhost:6379/0",
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0',
    CELERYBEAT_SCHEDULE = {
        'add-every-minute': {
        'task': 'app.scheduled_task',
        'schedule': crontab(minute='*'),
        }
    },
    CELERY_TIMEZONE='Asia/Shanghai'
)


# Celery configuration
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def scheduled_task(*args, **kwargs):
    print(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())))


@celery.task(bind=True)
def do_async_long_task(self, task_flag):
    print(task_flag + " start")
    delay_time = random.randint(5, 20)
    print(delay_time)
    for i in range(delay_time):
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': delay_time,
                                'status': "sleeping"})
        print(i)
        time.sleep(1)
    print(task_flag + " end")
    return {'current': 100, 'total': 100, 'status': 'awake!',
            'result': "done!"}


@app.route('/longtask', methods=['GET', 'POST'])
def longtask():
    # task = do_async_long_task.apply_async()
    task_flag = "task_" + str(random.randint(1, 100))
    task = do_async_long_task.apply_async(args=[task_flag])
    return jsonify({'Location': url_for('taskstatus', task_id=task.id),
                    'task_flag': task_flag})


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = do_async_long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 'calculating...',
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # 异常反馈
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
