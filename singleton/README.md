## singleton

一个单文件的flask+celery+redis的demo，实现通过http请求，利用celery协调redis队列异步执行，并提供接口可查看任务状态。

# 使用步骤
 - 安装redis。
 - 安装requirements.txt中的依赖。
 - 启动redis
 - 启动celery  
 `celery worker -A app.celery --loglevel=info`
- 启动app  
`python3 app.py`
- 新增任务：访问  http://127.0.0.1:5000/longtask
- 查看任务状态：访问http://127.0.0.1:5000/status/<task_id>

# 坑与建议
- 使用redis的celery安装可以通过如下命令一起安装：`pip3 install -U celery[redis]`   
但是redis3.0.1和celery4.2.1有冲突，需要降到redis2.10.5  
  
- 启动celery时可指定worker数：  
`venv/bin/celery worker -A app.celery --loglevel=info -C 1`
其中app.celery根据实际初始化celery的py文件定  
-C是指起几个worker，默认是根据cpu核数。
- celery启动时加载task，所以 task代码改动之后需重启celery，否则改动无效。