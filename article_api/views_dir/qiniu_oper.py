
from django.http import HttpResponse
from article_api.publicFunc import Response
import qiniu
from django.http import JsonResponse
from article_api import models
import requests

# 前端请求
def qiniu_oper(request, oper_type):
    response = Response.ResponseObj()
    if oper_type == 'get_token':

        SecretKey = 'wVig2MgDzTmN_YqnL-hxVd6ErnFhrWYgoATFhccu'
        AccessKey = 'a1CqK8BZm94zbDoOrIyDlD7_w7O8PqJdBHK-cOzz'
        q = qiniu.Auth(AccessKey, SecretKey)
        bucket_name = 'bjhzkq_tianyan'
        token = q.upload_token(bucket_name)  # 可以指定key 图片名称

        response.code = 200
        response.msg = '生成成功'
        response.data = {'token': token}

    return JsonResponse(response.__dict__)


# 发送报错提醒
def error_send_msg(request):
    msg = request.GET.get('msg')
    if msg:
        # url = 'http://zhugeleida.zhugeyingxiao.com/tianyan/outside_calls_send_msg?msg={}'.format(msg)
        url = 'http://127.0.0.1:8008/tianyan/api/outside_calls_send_msg?msg={}'.format(msg)
        requests.get(url)
    return HttpResponse('已发送 错误消息')




