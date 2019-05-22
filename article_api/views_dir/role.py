from article_api import models
from article_api.publicFunc import Response
from article_api.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from article_api.publicFunc.condition_com import conditionCom
from article_api.forms.role import AddForm, UpdateForm, SelectForm
from article_api.views_dir.permissions import init_data
import json


# cerf  token验证 用户展示模块
@csrf_exempt
@account.is_token(models.userprofile)
def role(request):
    response = Response.ResponseObj()
    if request.method == "GET":
        forms_obj = SelectForm(request.GET)
        if forms_obj.is_valid():

            current_page = forms_obj.cleaned_data['current_page']
            length = forms_obj.cleaned_data['length']
            print('forms_obj.cleaned_data -->', forms_obj.cleaned_data)

            order = request.GET.get('order', '-create_date')
            user_id = request.GET.get('user_id')
            userObjs = models.userprofile.objects.filter(id=user_id)

            field_dict = {
                'id': '',
                'name': '__contains',
                'create_date': '',
                'oper_user__username': '__contains',
            }
            q = conditionCom(request, field_dict)
            print('q -->', q)
            objs = models.role.objects.filter(q).order_by(order)
            count = objs.count()

            if length != 0:
                start_line = (current_page - 1) * length
                stop_line = start_line + length
                objs = objs[start_line: stop_line]

            ret_data = []
            for obj in objs:
                permissionsList = []
                if obj.permissions:
                    permissionsList = [i['id'] for i in obj.permissions.values('id')]
                    # if len(permissionsList) > 0:
                    #     permissionsData = init_data(selected_list=permissionsList)

                if obj.oper_user:
                    oper_user_id = obj.oper_user_id
                    oper_user_username = obj.oper_user.username
                else:
                    oper_user_username = ''
                    oper_user_id = ''

                ret_data.append({
                    'id': obj.id,
                    'name': obj.name,                           # 角色名称
                    'permissionsData': permissionsList,         # 角色权限
                    'oper_user_id': oper_user_id,               # 操作人ID
                    'oper_user__username': oper_user_username,  # 操作人
                    'create_date': obj.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                })

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


#  增删改
#  csrf  token验证
@csrf_exempt
@account.is_token(models.userprofile)
def role_oper(request, oper_type, o_id):
    response = Response.ResponseObj()

    if request.method == "POST":
        user_id = request.GET.get('user_id')

        # 添加角色
        if oper_type == "add":
            form_data = {
                'oper_user_id': request.GET.get('user_id'),             # 操作人ID
                'name': request.POST.get('name'),                       # 角色名称
                'permissionsList': request.POST.get('permissionsList'), # 角色权限
            }

            forms_obj = AddForm(form_data)
            if forms_obj.is_valid():
                obj = models.role.objects.create(**{
                    'name': forms_obj.cleaned_data.get('name'),
                    'oper_user_id': forms_obj.cleaned_data.get('oper_user_id'),
                })
                permissionsList = forms_obj.cleaned_data.get('permissionsList')
                obj.permissions = permissionsList
                obj.save()
                response.code = 200
                response.msg = "添加成功"
                response.data = {'testCase': obj.id}

            else:
                response.code = 301
                response.msg = json.loads(forms_obj.errors.as_json())

        # 修改角色
        elif oper_type == "update":
            form_data = {
                'o_id': o_id,
                'name': request.POST.get('name'),                           # 角色名称
                'oper_user_id': request.GET.get('user_id'),                 # 操作人ID
                'permissionsList': request.POST.get('permissionsList'),     # 角色权限
            }

            forms_obj = UpdateForm(form_data)
            if forms_obj.is_valid():
                o_id = forms_obj.cleaned_data['o_id']
                name = forms_obj.cleaned_data['name']                           # 角色名称
                oper_user_id = forms_obj.cleaned_data['oper_user_id']           # 操作人ID
                permissionsList = forms_obj.cleaned_data['permissionsList']     # 角色权限

                objs = models.role.objects.filter(
                    id=o_id
                )
                if objs:
                    objs.update(
                        name=name,
                        oper_user_id=oper_user_id,
                    )
                    objs[0].permissions = permissionsList
                    response.code = 200
                    response.msg = "修改成功"

                else:
                    response.code = 303
                    response.msg = '不存在的数据'

            else:
                response.code = 301
                response.msg = json.loads(forms_obj.errors.as_json())

        # 删除角色
        elif oper_type == "delete":
            objs = models.role.objects.filter(id=o_id)
            if objs:
                obj = objs[0]
                userObj = models.userprofile.objects.get(id=user_id)
                if userObj.role_id == obj.id:
                    response.code = 301
                    response.msg = '不能删除自己角色'

                else:
                    if models.userprofile.objects.filter(role_id=o_id):
                        response.code = 304
                        response.msg = '含有子级数据,请先删除或转移子级数据'

                    else:
                        objs.delete()
                        response.code = 200
                        response.msg = "删除成功"

            else:
                response.code = 302
                response.msg = '删除ID不存在'

    else:

        if oper_type == "get_rules":
            objs = models.role.objects.filter(id=o_id)
            if objs:
                obj = objs[0]
                rules_list = [i['name'] for i in obj.permissions.values('name')]
                response.data = {
                    'rules_list': rules_list
                }
                response.code = 200
                response.msg = "查询成功"

        else:
            response.code = 402
            response.msg = "请求异常"

    return JsonResponse(response.__dict__)
