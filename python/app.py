from flask import Flask
from celery import Celery
import time
import random


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/0"
app.config['CELERY_RESULT_BACKEND'] = "redis://localhost:6379/0"


# Celery configuration
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def do_async_task(msg):
    print(msg)


@celery.task(bind=True)
def do_async_long_task(self, task_id):
    delay_time = random.randint(5, 20)
    self.update_state(state='PROGRESS', meta={'delay_time': delay_time})
    time.sleep(delay_time)
    return task_id + "done!"


@app.route('/longtask', methods=['POST'])
def longtask():
    task_flag = random.randint(1, 100)
    task = do_async_long_task.apply_async(args=[task_flag])
    return "task_flag:" + str(task_flag) + ",task_id:" + str(task.id)


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
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
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
