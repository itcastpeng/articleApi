from article_api import models
from article_api.publicFunc import Response
from article_api.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from article_api.publicFunc.condition_com import conditionCom
from article_api.forms.permissions import AddForm, UpdateForm, SelectForm
import json


def init_data(pid=None, selected_list=None):
    # print('pid-------------> ', pid)
    """
    获取权限数据
    :param pid:  权限父级id
    :return:
    """
    result_data = []
    objs = models.permissions.objects.filter(pid_id=pid)
    for obj in objs:
        current_data = {
            'name': obj.name,
            'title': obj.title,
            'expand': True,
            'id': obj.id,
            'checked': False
        }
        if selected_list and obj.id in selected_list:
            current_data['checked'] = True
        children_data = init_data(obj.id, selected_list)
        if children_data:
            current_data['children'] = children_data
        result_data.append(current_data)

    return result_data


# cerf  token验证 用户展示模块
@csrf_exempt
@account.is_token(models.userprofile)
def permissions(request):
    response = Response.ResponseObj()
    if request.method == "GET":
        forms_obj = SelectForm(request.GET)
        if forms_obj.is_valid():

            current_page = forms_obj.cleaned_data['current_page']
            length = forms_obj.cleaned_data['length']
            print('forms_obj.cleaned_data -->', forms_obj.cleaned_data)
            order = request.GET.get('order', '-create_date')
            field_dict = {
                'id': '',
                'name': '__contains',
                'create_date': '',
                'oper_user__username': '__contains',
                'pid_id': '__isnull'
            }
            q = conditionCom(request, field_dict)
            print('q -->', q)

            objs = models.permissions.objects.select_related('pid').filter(q).order_by(order)
            count = objs.count()

            if length != 0:
                start_line = (current_page - 1) * length
                stop_line = start_line + length
                objs = objs[start_line: stop_line]

            ret_data = []
            for obj in objs:
                #  如果有oper_user字段 等于本身名字
                if obj.oper_user:
                    oper_user_id = obj.oper_user_id
                    oper_user_username = obj.oper_user.username
                else:
                    oper_user_username = ''
                    oper_user_id = ''

                pid_name = ''
                if obj.pid:
                    pid_name = obj.pid.name
                ret_data.append({
                    'id': obj.id,
                    'name': obj.name,               # 权限名字
                    'title': obj.title,             # 权限路径
                    'pid_id': obj.pid_id,           # 权限父级ID
                    'pid_name': pid_name,           # 权限父级名称
                    'oper_user_id': oper_user_id,   # 操作人ID
                    'oper_user__username': oper_user_username, # 操作人
                    'create_date': obj.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                })
            #  查询成功 返回200 状态码
            response.code = 200
            response.msg = '查询成功'
            response.data = {
                'ret_data': ret_data,
                'data_count': count,
            }
            response.note = {
                'ret_data': {
                    'id': '权限ID',
                    'name': '权限名字',
                    'title': '权限路径',
                    'pid_id': '权限父级ID',
                    'pid_name': '权限父级名称',
                    'oper_user_id': '操作人ID',
                    'oper_user__username': '操作人',
                    'create_date': '创建时间',
                },
                'data_count': '数据总数',
            }

        else:
            response.code = 301
            response.data = json.loads(forms_obj.errors.as_json())
    else:
        response.code = 402
        response.msg = "请求异常"
    return JsonResponse(response.__dict__)


#  增删改
#  csrf  token验证
@csrf_exempt
@account.is_token(models.userprofile)
def permissions_oper(request, oper_type, o_id):
    response = Response.ResponseObj()
    user_id = request.GET.get('user_id')
    if request.method == "POST":

        # 创建权限
        if oper_type == "add":
            form_data = {
                'oper_user_id': request.GET.get('user_id'), # 操作人ID
                'name': request.POST.get('name'),           # 权限名称
                'title': request.POST.get('title'),         # 权限路径
                'pid_id': request.POST.get('pid_id'),       # 权限父级ID
            }
            forms_obj = AddForm(form_data)
            if forms_obj.is_valid():
                models.permissions.objects.create(**forms_obj.cleaned_data)
                response.code = 200
                response.msg = "添加成功"

            else:
                response.code = 301
                response.msg = json.loads(forms_obj.errors.as_json())

        # 修改权限
        elif oper_type == "update":
            form_data = {
                'o_id': o_id,
                'name': request.POST.get('name'),               # 权限名称
                'title': request.POST.get('title'),             # 权限路径
                'pid_id': request.POST.get('pid_id'),           # 权限父级ID
                'oper_user_id': request.GET.get('user_id'),     # 操作人ID
            }

            forms_obj = UpdateForm(form_data)
            if forms_obj.is_valid():
                o_id = forms_obj.cleaned_data['o_id']
                name = forms_obj.cleaned_data['name']                   # 权限名称
                title = forms_obj.cleaned_data['title']                 # 权限路由
                pid_id = forms_obj.cleaned_data['pid_id']               # 权限父级ID
                oper_user_id = forms_obj.cleaned_data['oper_user_id']   # 操作人ID
                models.permissions.objects.filter(id=o_id).update(
                    name=name,
                    title=title,
                    pid_id=pid_id,
                    oper_user_id=oper_user_id,
                )
                response.code = 200
                response.msg = "修改成功"

            else:
                response.code = 301
                response.msg = json.loads(forms_obj.errors.as_json())

        # 删除权限
        elif oper_type == "delete":
            objs = models.permissions.objects.filter(id=o_id)
            if objs:
                obj = objs[0]
                if models.permissions.objects.filter(pid_id=obj.id).count() > 0:
                    response.code = 304
                    response.msg = "含有子级数据,请先删除或转移子级数据"

                else:
                    objs.delete()
                    response.code = 200
                    response.msg = "删除成功"
            else:
                response.code = 302
                response.msg = '删除ID不存在'

    else:

        # 获取tree数据成功
        if oper_type == "get_tree_data":
            response.code = 200
            response.msg = "获取tree数据成功"
            response.data = {
                'ret_data': init_data()
            }

        # 获取该用户所有权限
        elif oper_type == 'get_permissions':
            user_obj = models.userprofile.objects.filter(id=user_id)
            if user_obj:
                role_obj = models.role.objects.filter(id=user_obj[0].role_id)
                data_list = []
                for i in role_obj[0].permissions.all():
                    data_list.append({
                        'id':i.id,
                        'name':i.name,
                        'title':i.title,
                    })
                response.code = 200
                response.msg = '查询成功'
                response.data = data_list
            else:
                response.code = 301
                response.msg = '非法用户'

        else:
            response.code = 402
            response.msg = "请求异常"

    return JsonResponse(response.__dict__)
