

BROKER_URL = 'redis://123456@localhost:6379/1'

CELERY_RESULT_BACKEND = 'redis://123456@localhost:6379/2'

CELERY_IMPORTS = (
    'apps.ansible_command',
    'apps.ansible_playbook',
    'apps.command',
)

#时区的设置
CELERY_TIMEZONE = 'Asia/Shanghai'

#是否使用本地的时区
CELERY_ENABLE_UTC = False

# #重写Task的属性
# CELERY_TASK_ANNOTATIONS = {'apps.task1.add':{'rate_limit':'10/s'}}
#
#链接错误情况下是否重试发布任务消息,默认为True
CELERY_TASK_PUBLISH_RETRY = False
#
#并发的worker数量
CELERY_CONCURRENCY = 4
#
#每次worker去任务队列中取的任务数量
CELERY_PREFETH_MULTIPLIRE = 5
#
#每个worker执行多少次就会被杀掉
CELERY_MAX_TASKS_PER_CHILD = 4
#
#单个任务的最大执行时间
CELERY_TASK_TIME_LIMIT = 60*3

#celery任务执行结果的超时时间
CELERY_TASK_RESULT_EXPIRES =1000


from kombu import Queue
CELERY_QUEUES = (
    Queue('task2_subs',routing_key='task2_subs'),
    Queue('beat_task',routing_key='beat_task'),
    Queue('spider_queue',routing_key='spider_queue')
)

CELERY_ROUTES ={
    'apps.task2.subs':{'queue':'task2_subs','routing_key':'task2_subs'}
}


