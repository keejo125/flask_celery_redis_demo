## factory

一个工厂模式的flask+celery+redis的demo，实现通过http请求，利用celery协调redis队列异步执行，并提供接口可查看任务状态。

# 使用步骤
 - 安装redis。
 - 安装requirements.txt中的依赖。
 - 启动redis
 - 启动celery  
 `celery worker -A celery_app.celery --loglevel=info`
- 启动app
- 新增任务：访问  http://127.0.0.1:5000/longtask
- 查看任务状态：访问http://127.0.0.1:5000/status/<task_id>

# 坑与建议
- windows环境中celery4不支持，需要降到celery3。
- celery模块和flask模块可单独部署，在flask模块中直接从celery模块中导入celery来声明celery任务。celery模块中需在配置时使用include来显示声明celery任务所在的包，否则会出现celery启动无法加载任务的问题。
- 在配置celery中的redis时，`broker='redis://localhost:6379/1',`中的1指的是redis的1号数据库，一个库只能连一个celery，否则第二个celery连接时会崩溃。默认是0号库。
- 使用redis的celery安装可以通过如下命令一起安装：`pip3 install -U celery[redis]`   
但是redis3.0.1和celery4.2.1有冲突，需要降到redis2.10.5  
  
- 启动celery时可指定worker数：  
`celery worker -A app.celery --loglevel=info -C 1`  
其中app.celery根据实际初始化celery的py文件定  
-C是指起几个worker，默认是根据cpu核数。
- celery启动时加载task，所以 task代码改动之后需重启celery，否则改动无效。