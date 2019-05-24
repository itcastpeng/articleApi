from django.http import HttpResponse, JsonResponse
from article_api.publicFunc.Response import ResponseObj
from article_api import models
from article_api.publicFunc.public import data_statistics_get_article, time_screen


# 首页数据统计
def data_statistics(request, oper_type):
    res = ResponseObj()

    # 文章分类占比
    if oper_type == 'article_classify_account':

        objs = models.classfiy.objects.filter(
            parent_class__isnull=True,
            create_date__isnull=False
        )

        data_list = []
        article_count = 0 # 文章总数

        for obj in objs:
            clsas_id = obj.id

            first_num = models.article.objects.filter(classfiy=clsas_id).count()
            num = data_statistics_get_article(0, clsas_id)
            classify_count = first_num + num # 单个分类总数
            data_list.append({
                'classify_id': obj.id,
                'classify_name': obj.classify_name,
                'classify_count': classify_count,

            })
            article_count += classify_count

        ret_data = []
        for data in data_list:
            avg = (data.get('classify_count') / article_count) * 100 # 百分比

            ret_data.append({
                'classify_id': data.get('classify_id'),
                'classify_name': data.get('classify_name'),
                'avg': avg,
            })


        res.code = 200
        res.msg = '查询成功'
        res.data = {
            'ret_data': ret_data,
            'article_count': article_count
        }
        res.note = {
            'article_count': '文章总数',
            'ret_data 文章分类占比': {
                'classify_id': '文章分类ID',
                'classify_name': '文章分类名称',
                'avg': '文章分类占比',
            },
        }

    # 文章增加数量
    elif oper_type == 'article_add_num':

        number_days = request.GET.get('number_days')
        time_data_list = time_screen(number_days)
        ret_data = []
        for time_data in time_data_list:

            objs_count = models.article.objects.filter(
                create_date__isnull=False,
                create_date__gte=time_data.get('start_time'),
                create_date__lte=time_data.get('stop_time')
            ).count()

            ret_data.append({
                'objs_count': objs_count,
                'date': time_data.get('ymd')
            })

        res.code = 200
        res.msg = '查询成功'
        res.data = {
            'ret_data': ret_data,
        }
        res.note = {
            'ret_data 数据':{
                'objs_count': '当天 添加文章篇数',
                'date': '当天 添加文章日期 年月日(Y-m-d)'
            }
        }

    return JsonResponse(res.__dict__)




























