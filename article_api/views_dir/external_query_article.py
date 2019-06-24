from article_api import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from article_api.publicFunc.condition_com import conditionCom
from article_api.publicFunc import Response, account
from article_api.publicFunc.public import query_classification_supervisor
from article_api.forms.external_query_article import SelectForm
import json



@csrf_exempt
def external_query_article(request, oper_type):
    response = Response.ResponseObj()
    if request.method == "GET":

        # 查询公开文章
        if oper_type == 'article':
            forms_obj = SelectForm(request.GET)
            if forms_obj.is_valid():
                current_page = forms_obj.cleaned_data['current_page']
                length = forms_obj.cleaned_data['length']

                order = request.GET.get('order', '-create_date')
                field_dict = {
                    'id': '',
                    'title': '__contains',
                    'create_date': '__contains',
                    'article_source': '',
                    # 'oper_user__username': '__contains',
                }
                q = conditionCom(request, field_dict)

                objs = models.article.objects.filter(q, toward_whether=1).order_by(order).exclude(is_delete=1)
                count = objs.count()

                if length != 0:
                    start_line = (current_page - 1) * length
                    stop_line = start_line + length
                    objs = objs[start_line: stop_line]

                ret_data = []
                id = request.GET.get('id')
                for obj in objs:
                    classfiy_id = obj.classfiy_id
                    classfiy_name = obj.classfiy.classify_name
                    result_data = {
                        'id': obj.id,
                        'title': obj.title,  # 文章标题
                        'summary': obj.summary,  # 文章摘要
                        'article_cover': obj.article_cover,                             # 文章封面图
                        'edit_name': obj.edit_name,                                     # 作者别名
                        'article_source_id': obj.article_source,                        # 文章来源ID
                        'article_source': obj.get_article_source_display(),             # 文章来源
                        # 'stop_upload': obj.stop_upload,                                 # 是否停止发布
                        'classfiy_id': classfiy_id,                                     # 分类ID
                        'classfiy_name': classfiy_name,                                 # 分类名称
                        'article_word_count': obj.article_word_count,                   # 文章字数
                        'create_date': obj.create_date.strftime('%Y-%m-%d %H:%M:%S'),   # 文章创建时间
                    }

                    if id:
                        result_data['content'] = obj.content                             # 文章内容
                        class_list = []
                        class_list = query_classification_supervisor(classfiy_id, class_list)

                        result_data['classfiy_list'] = class_list                       # 分类所有等级

                    ret_data.append(result_data)

                article_source = []
                for i in models.article.article_source_choices:
                    article_source.append({
                        'id':i[0],
                        'name':i[1]
                    })

                #  查询成功 返回200 状态码
                response.code = 200
                response.msg = '查询成功'
                response.data = {
                    'ret_data': ret_data,
                    'data_count': count,
                    'article_source':article_source # 文章来源

                }

            else:
                response.code = 301
                response.data = json.loads(forms_obj.errors.as_json())

        else:
            response.code = 402
            response.msg = "请求异常"

    else:
        response.code = 402
        response.msg = "请求异常"
    return JsonResponse(response.__dict__)

