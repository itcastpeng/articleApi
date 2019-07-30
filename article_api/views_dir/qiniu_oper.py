
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
    response = Response.ResponseObj()
    # msg = request.GET.get('msg')
    # if msg:
    #     url = 'http://zhugeleida.zhugeyingxiao.com/tianyan/api/outside_calls_send_msg?msg={}&external=1'.format(msg)
    #     # url = 'http://127.0.0.1:8008/tianyan/api/outside_calls_send_msg?msg={}&external=1'.format(msg)
    #     requests.get(url)
    #
    # response.code = 200
    # response.msg = '已发送错误消息'
    url = request.GET.get('url')

    return JsonResponse(response.__dict__)



def get_yuemei_case(request):
    response = Response.ResponseObj()
    objs = models.yuemei.objects.filter(is_use=0).order_by('create_date')
    if objs:
        obj = objs[0]
        obj.is_use = 1
        obj.save()

        response.code = 200
        response.data = obj.url

    else:
        response.code = 301
    # url = request.GET.get('url')
    # objs = models.yuemei.objects.filter(url=url)
    # if not objs:
    #     models.yuemei.objects.create(url=url)
    return JsonResponse(response.__dict__)



# def test(request):
#     title = """
#         鼻部整形
#         眼部整形
#         胸部整形
#         面部轮廓
#         唇部整形
#         除皱
#         牙齿美容
#         微创注射
#         无创激光
#         纹绣
#         脂肪
#         私密整形
#         毛发种植
#
#         """
#     for i in title.split('\n'):
#         title = i.replace('\r\n', '').replace('\n', '').strip()
#         if title:
#             print('title----> ', title)
#             obj = models.classfiy.objects.create(
#                 oper_user_id=6,
#                 parent_class_id=435,
#                 classify_name=title,
#                 level=2
#             )
#             print('title-----> ', obj.id, title)
#             models.classfiy.objects.create(
#                 oper_user_id=6,
#                 parent_class_id=obj.id,
#                 classify_name=title,
#                 level=3
#             )
#
#     return HttpResponse('')














