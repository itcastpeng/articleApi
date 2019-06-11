"""articleApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from article_api.views_dir import login, user, permissions, role, settlement_rules, article, \
    classfiy, data_statistics, qiniu_oper

urlpatterns = [

    # celery 路由
    url(r'^celery/', include('article_api.views_dir.celery.urls')),

    # 数据统计
    url(r'^data_statistics/(?P<oper_type>\w+)$', data_statistics.data_statistics),

    # 账号密码登录
    url(r'^login$', login.login),

    # 用户
    url(r'^user/(?P<oper_type>\w+)/(?P<o_id>\d+)$', user.user_oper),
    url(r'^updatePwd$', user.updatePwd),
    url(r'^user$', user.user),

    # 权限管理
    url(r'^permissions/(?P<oper_type>\w+)/(?P<o_id>\d+)$', permissions.permissions_oper),
    url(r'^permissions$', permissions.permissions),

    # 角色管理
    url(r'^role/(?P<oper_type>\w+)/(?P<o_id>\d+)$', role.role_oper),
    url(r'^role$', role.role),

    # 分类管理
    url(r'^classfiy/(?P<oper_type>\w+)/(?P<o_id>\d+)$', classfiy.classfiy_oper),
    url(r'^classfiy', classfiy.classfiy),

    # 文章管理
    url(r'^article/(?P<oper_type>\w+)/(?P<o_id>\d+)$', article.article_oper),
    url(r'^article$', article.article),

    # 七牛云
    url(r'^qiniu/(?P<oper_type>\w+)$', qiniu_oper.qiniu_oper),

    # 错误 提示
    url(r'^error_send_msg$', qiniu_oper.error_send_msg),




    # celery 执行视图
    # url(r'^send_article$', celery_views.send_article),  # 上传文章
    # url(r'^test$', qiniu_oper.test),
]


