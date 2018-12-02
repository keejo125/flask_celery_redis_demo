## factory

一个工厂模式的flask+celery+redis的demo，实现通过http请求，利用celery协调redis队列异步执行，并提供接口可查看任务状态。

# 使用步骤
 - 安装redis。
 - 安装requirements.txt中的依赖。
 - 启动redis
 - 启动celery  
 `celery worker -A manager.celery --loglevel=info`
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

- 关于celery中使用flask上下文的问题。参考了网上好多材料，都弄的不是很清楚。主要问题就是，celery使用flask上下文需要重写celery的task。
    - 尝试方法一：
    直接在任务中使用`with app.app_context()`会提示`RuntimeError: Working outside of application context.`，
    - 尝试方法二：
    在celery任务中直接传入app对象，结果发现`delay()`只能传入json格式，不支持传入对象。
    - 尝试方法三：
    最后查看flask官网的[说明](http://flask.pocoo.org/docs/1.0/patterns/celery/),给出了一段重写celery.task的代码，但例子中是所有的声明，引用都在单文件中，不存在循环引用的问题，但思路应该是对的。最终尝试可行的方案如下：
        - 1、在app同级建立一个celery_app，配置和创建一个celery对象，用于给flask提供celery的导入(task和app的初始化)。
        - 2、在app的构建函数`__init__.py`中参考官网提供一共`make_celery`的函数重写celery的task。
        - 3、在最外层入口`manager.py`中，执行`make_celery`来给celery的task增加上下文。
        - 4、最后启动celery的时候需要启动`manager.py`中的celery对象（已经重写了task的celery）。
        - 5、运行成功。不知道有没有讲清楚，如果理解有偏差，也请指正。