# -*- coding: utf-8 -*-
from flask import Flask, jsonify, url_for
import random
from . import main
from .tasks import main_task


@main.route('/longtask', methods=['GET', 'POST'])
def longtask():
    # task = do_async_long_task.apply_async()
    task_flag = "task_" + str(random.randint(1, 100))
    task = main_task.apply_async(args=[task_flag])
    return jsonify({'Location': url_for('main.taskstatus', task_id=task.id),
                    'task_flag': task_flag})


@main.route('/status/<task_id>')
def taskstatus(task_id):
    task = main_task.AsyncResult(task_id)
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