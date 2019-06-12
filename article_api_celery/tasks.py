from __future__ import absolute_import, unicode_literals
from .celery import app
from article_api.publicFunc.host import URL
import requests, datetime



@app.task
def update_article():
    print('-----------------------------------celery-----------------> ', datetime.datetime.today())
    url = '{}/celery/celery_regularly_update_articles'.format(URL)
    requests.get(url)















