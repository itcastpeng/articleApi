
from article_api import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Q
import requests, time, datetime

# token认证
def article_params():
    token = '93b5f91eb56b8a4f8d96b7182920d68d'
    timestamp = str(int(time.time() * 1000))
    get_data = {
        'rand_str': account.str_encrypt(timestamp + token),
        'timestamp': timestamp,
        'user_id': 1,
    }
    return get_data

host = 'http://192.168.10.170:8001/'
# host = 'http://api.zhugeyingxiao.com/'

# 上传文章
@csrf_exempt
def send_article(request):
    response = Response.ResponseObj()
    now_data = datetime.datetime.today()
    deletionTime = (now_data - datetime.timedelta(minutes=30))  #

    objs = models.article.objects.filter(
        is_send=0,
        leida_article_id__isnull=True,
        create_date__lte=deletionTime,       # 编辑上传三十分钟后才上传
        stop_upload=0,                       # 避开停止发布
    ).order_by('create_date')
    if objs:
        obj = objs[0]
        print('obj.id-----> ', obj.id)
        data = {
            'title':obj.title,
            'summary':obj.summary,
            'content':obj.content,
            'edit_name':obj.edit_name,
        }
        url = '{}zhugeleida/admin/article/sync_local_article'.format(host)
        ret = requests.post(url, data=data, params=article_params())
        if int(ret.json().get('code')) == 200:
            article_id = ret.json().get('data').get('article_id')
            obj.is_send = 1
            obj.leida_article_id = article_id
            obj.save()
        response.code = ret.json().get('code')
        response.msg = ret.json().get('msg')
    return JsonResponse(response.__dict__)


# 文章阅读详情
@csrf_exempt
def article_read_detail(request):
    response = Response.ResponseObj()
    now_data = datetime.datetime.today()
    q = Q()
    q.add(Q(last_query_time__isnull=True) | Q(last_query_time__lte=now_data), Q.AND)
    objs = models.article.objects.filter(q).order_by('create_date')
    if objs:
        obj = objs[0]
        print('obj.id--------------> ', obj.id, obj.leida_article_id)
        url = '{}zhugeleida/admin/article/query_local_article_readinfo'.format(host)
        params = article_params()
        params['article_id'] = obj.leida_article_id

        ret = requests.get(url, params=params)
        print('ret.json()-----------> ', ret.json())
        ret_json = ret.json().get('data')
        if int(ret.json().get('code')) == 200:
            deletionTime = (now_data + datetime.timedelta(days=1))  # 当前时间加上一天(文章阅读详情每隔一天查询更新一次)
            read_count = ret_json.get('read_count')             # 阅读量
            stay_time = ret_json.get('stay_time')               # 阅读时长

            read_count = obj.reading_num + read_count
            stay_time = obj.reading_time + stay_time

            obj.last_query_time = deletionTime
            obj.reading_num = read_count
            obj.reading_time = stay_time
            obj.save()

    response.code = 200
    response.msg = '查询成功'
    return JsonResponse(response.__dict__)
