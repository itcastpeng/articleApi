from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab

app = Celery(
    broker='redis://redis_host:6379/3',
    backend='redis://redis_host:6379/3',
    include=['article_api_celery.tasks'],

)
app.conf.enable_utc = False
app.conf.timezone = "Asia/Shanghai"
CELERYD_FORCE_EXECV = True    # 非常重要,有些情况下可以防止死锁
CELERYD_MAX_TASKS_PER_CHILD = 100    # 每个worker最多执行万100个任务就会被销毁，可防止内存泄露
app.conf.beat_schedule = {

    # 更新文章 (10分钟一次)
    'update_article':{
        'task':'article_api_celery.tasks.update_article',
        # 'schedule': crontab("0", '*/1', '*', '*', '*'),  # 此处跟 linux 中 crontab 的格式一样
        'schedule': crontab(minute='*/10'),  # 直接写个10为1小时执行一次  */10 为 十分钟一次
        'args':[] # # 传入任务函数的参数,可以是一个列表或元组,如果函数没参数则为空列表或空元组
    },



}
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
