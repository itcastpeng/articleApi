
from django.conf.urls import url
from article_api.views_dir.celery import celery_public



urlpatterns = [


    # 调用 下载资源到本地
    url(r'^download_inter/(?P<oper_type>\w+)$', celery_public.download_inter),


]



























