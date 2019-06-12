
from django.conf.urls import url
from article_api.views_dir.celery import celery_public



urlpatterns = [


    # 定时更新 文章
    url(r'^celery_regularly_update_articles$', celery_public.celery_regularly_update_articles),


]



























