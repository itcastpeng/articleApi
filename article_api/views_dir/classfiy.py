from article_api import models
from article_api.publicFunc import Response
from article_api.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from article_api.publicFunc.condition_com import conditionCom
from article_api.forms.classfiy import AddForm, UpdateForm, SelectForm
from article_api.publicFunc import public
import json
from article_api.publicFunc.public import Classification_judgment, query_classification_supervisor

# cerf  token验证 分类查询
@csrf_exempt
@account.is_token(models.userprofile)
def classfiy(request):
    response = Response.ResponseObj()
    if request.method == "GET":
        forms_obj = SelectForm(request.GET)
        if forms_obj.is_valid():

            current_page = forms_obj.cleaned_data['current_page']
            length = forms_obj.cleaned_data['length']

            order = request.GET.get('order', '-create_date')
            user_id = request.GET.get('user_id')

            field_dict = {
                'id': '',
                'level': '',
                'classify_name': '__contains',
                'parent_class_id': '',
                'oper_user_id': '',
            }
            q = conditionCom(request, field_dict)
            print('q -->', q)


            objs = models.classfiy.objects.filter(q, oper_user__isnull=False)
            count = objs.count()

            if length != 0:
                start_line = (current_page - 1) * length
                stop_line = start_line + length
                objs = objs[start_line: stop_line]

            # 返回的数据
            ret_data = []
            for obj in objs:

                parent_id = ''
                parent_name = ''
                class_list = []
                if obj.parent_class:
                    parent_id = obj.parent_class_id
                    parent_name = obj.parent_class.classify_name

                    class_list = query_classification_supervisor(parent_id, class_list)

                ret_data.append({
                    'id': obj.id,
                    'name': obj.classify_name,                          # 分类名称
                    'parent_id': parent_id,                             # 父级ID
                    'parent_name': parent_name,                         # 父级分类名称
                    'level': obj.level,                                 # 父级分类名称
                    'oper_user_id': obj.oper_user_id,                   # 操作人ID
                    'oper_user__username': obj.oper_user.username,      # 操作人
                    'class_list': class_list,                           # 所有分类
                    'create_date': obj.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                })

            #  查询成功 返回200 状态码
            response.code = 200
            response.msg = '查询成功'
            response.data = {
                'ret_data': ret_data,
                'data_count': count,
            }

        else:
            response.code = 402
            response.msg = "请求异常"
            response.data = json.loads(forms_obj.errors.as_json())

    return JsonResponse(response.__dict__)


#  分类增删改
#  csrf  token验证
@csrf_exempt
@account.is_token(models.userprofile)
def classfiy_oper(request, oper_type, o_id):
    response = Response.ResponseObj()

    if request.method == "POST":
        user_id = request.GET.get('user_id')

        form_data = {
            'o_id': o_id,                                           # 操作ID
            'oper_user_id': user_id,                                # 操作人ID
            'classify_name': request.POST.get('classify_name'),     # 分类名称
            'parent_class': request.POST.get('parent_class'),       # 父级分类 ID
        }

        # 添加分类
        if oper_type == "add":
            #  创建 form验证 实例（参数默认转成字典）
            forms_obj = AddForm(form_data)
            if forms_obj.is_valid():
                form_clean_data = forms_obj.cleaned_data
                oper_user_id = form_clean_data.get('oper_user_id')
                classify_name = form_clean_data.get('classify_name')

                parent_class = ''
                num = 1
                if form_clean_data.get('parent_class'):
                    parent_class, num = form_clean_data.get('parent_class')

                objs = models.classfiy.objects.filter(level=num, classify_name=classify_name)
                if objs:
                    response.code = 301
                    response.msg = '{num}级分类已存在该名称'.format(num=num)

                else:
                    models.classfiy.objects.create(
                        oper_user_id=oper_user_id,
                        classify_name=classify_name,
                        parent_class_id=parent_class,
                        level=num
                    )

                    response.code = 200
                    response.msg = "添加成功"

            else:
                response.code = 301
                response.msg = json.loads(forms_obj.errors.as_json())

        # 修改分类
        elif oper_type == "update":
            forms_obj = UpdateForm(form_data)
            if forms_obj.is_valid():
                form_clean_data = forms_obj.cleaned_data
                o_id, objs = form_clean_data.get('o_id')
                oper_user_id = form_clean_data.get('oper_user_id')
                classify_name = form_clean_data.get('classify_name')

                parent_class = ''
                classifiy_level = 1
                if form_clean_data.get('parent_class'):
                    parent_class, classifiy_level = form_clean_data.get('parent_class')

                objs.update(
                    oper_user_id=oper_user_id,
                    classify_name=classify_name,
                    parent_class_id=parent_class,
                    level=classifiy_level
                )
                response.code = 200
                response.msg = '修改成功'

            else:
                response.code = 301
                response.msg = json.loads(forms_obj.errors.as_json())

        # 删除
        elif oper_type == "delete":
            # 删除 ID
            objs = models.classfiy.objects.filter(id=o_id)
            if objs:
                child_objs = models.classfiy.objects.filter(parent_class_id=o_id)
                if not child_objs:
                    if models.article.objects.filter(classfiy_id=o_id):
                        response.code = 301
                        response.msg = '该分类下存在文章'
                    else:
                        objs.delete()
                        response.code = 200
                        response.msg = '删除成功'

                else:
                    response.code = 301
                    response.msg = '含有子级分类'

            else:
                response.code = 301
                response.msg = '删除ID不存在'

    else:

        # 查询分类树状图
        if oper_type == 'get_tree':
            result_data = public.GroupTree()

            response.code = 200
            response.msg = '查询成功'
            response.data = {'ret_data': result_data}

        response.code = 402
        response.msg = "请求异常"

    return JsonResponse(response.__dict__)
