from article_api import models
from article_api.publicFunc import Response, account, the_output
from article_api.publicFunc.the_output import success_output_msg, error_output_msg, output_msg
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from article_api.publicFunc.condition_com import conditionCom
from article_api.forms.article import AddForm, UpdateForm, SelectForm, DeleteForm
import json, datetime, requests, time

# cerf  token验证 用户展示模块
@csrf_exempt
@account.is_token(models.userprofile)
def article(request):
    response = Response.ResponseObj()
    if request.method == "GET":
        forms_obj = SelectForm(request.GET)
        if forms_obj.is_valid():
            current_page = forms_obj.cleaned_data['current_page']
            length = forms_obj.cleaned_data['length']

            order = request.GET.get('order', '-create_date')
            field_dict = {
                'id': '',
                'name': '__contains',
                'create_date': '',
                'oper_user__username': '__contains',
            }
            q = conditionCom(request, field_dict)
            output_msg(q, out='q')

            objs = models.article.objects.filter(q).order_by(order).exclude(is_delete=1)
            count = objs.count()

            if length != 0:
                start_line = (current_page - 1) * length
                stop_line = start_line + length
                objs = objs[start_line: stop_line]

            # 返回的数据
            ret_data = []

            for obj in objs:

                #  将查询出来的数据加入列表
                ret_data.append({
                    'id': obj.id,
                    'title': obj.title,                                             # 文章标题
                    'summary': obj.summary,                                         # 文章摘要
                    'content': obj.content,                                         # 文章内容
                    'articlePic': obj.articlePic,                                   # 文章缩略图
                    'create_date': obj.create_date.strftime('%Y-%m-%d %H:%M:%S'),   # 文章创建时间
                })


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
    return JsonResponse(response.__dict__)


#  增删改
@csrf_exempt
@account.is_token(models.userprofile)
def article_oper(request, oper_type, o_id):
    response = Response.ResponseObj()
    user_id = request.GET.get('user_id')
    if request.method == "POST":

        form_data = {
            'o_id':o_id,
            'belongToUser_id': request.GET.get('user_id'),          # 操作人ID
            'title': request.POST.get('title'),                     # 文章标题
            'article_source': request.POST.get('article_source'),   # 文章来源
            'summary': request.POST.get('summary'),                 # 文章摘要
            'content': request.POST.get('content'),                 # 文章内容
            'articlePic': request.POST.get('articlePic'),           # 文章图片
            'edit_name': request.POST.get('edit_name'),             # 编辑别名
        }
        output_msg(form_data, out='form_data')

        # 添加文章
        if oper_type == "add":
            forms_obj = AddForm(form_data)
            if forms_obj.is_valid():
                success_output_msg("添加文章-验证通过")
                obj = models.article.objects.create(**forms_obj.cleaned_data)
                response.code = 200
                response.msg = "添加成功"
                response.data = {'testCase': obj.id}
            else:
                error_output_msg("添加文章-验证不通过")
                response.code = 301
                response.msg = json.loads(forms_obj.errors.as_json())

        # 修改文章
        elif oper_type == "update":
            forms_obj = UpdateForm(form_data)
            if forms_obj.is_valid():
                success_output_msg("修改文章-验证通过")
                o_id, obj = forms_obj.cleaned_data.get('o_id')
                obj.update(**{
                    'title':forms_obj.cleaned_data.get('title'),
                    'summary':forms_obj.cleaned_data.get('summary'),
                    'content':forms_obj.cleaned_data.get('content'),
                    'article_source':forms_obj.cleaned_data.get('article_source'),# 文章来源
                    'articlePic':forms_obj.cleaned_data.get('articlePic'),      # 文章缩略图
                    'edit_name':forms_obj.cleaned_data.get('edit_name'),        # 编辑别名
                })
                response.code = 200
                response.msg = '修改成功'
            else:
                error_output_msg("修改文章-验证不通过")
                response.code = 301
                response.msg = json.loads(forms_obj.errors.as_json())

        # 删除文章
        elif oper_type == "delete":
            forms_obj = DeleteForm(form_data)
            if forms_obj.is_valid():
                success_output_msg('删除文章-验证通过')
                o_id, obj = forms_obj.cleaned_data.get('o_id')
                obj[0].is_delete = 1
                obj[0].save()
                response.code = 200
                response.msg = '删除成功'
            else:
                error_output_msg("删除文章-验证不通过")
                response.code = 301
                response.msg = json.loads(forms_obj.errors.as_json())

    else:

        # 停止发布
        if oper_type == 'stop_upload':
            objs = models.article.objects.filter(id=o_id)
            if not objs:
                response.code = 301
                response.msg = '文章未找到'
            else:
                if objs[0].belongToUser_id == user_id:
                    if int(objs[0].is_send) != 0:
                        response.code = 301
                        response.msg = '该文章已上传, 如有疑问请联系管理员'
                    else:
                        if int(objs[0].stop_upload) == 0:
                            objs.update(
                                stop_upload=1
                            )
                            msg = '停止发布成功'
                        else:
                            objs.update(
                                stop_upload=0
                            )
                            msg = '开始发布成功'
                        response.code = 200
                        response.msg = msg
                else:
                    response.code = 301
                    response.msg = '权限不足'
        else:
            response.code = 402
            response.msg = "请求异常"

    return JsonResponse(response.__dict__)

