from article_api import models
from article_api.publicFunc import Response, account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from article_api.publicFunc.condition_com import conditionCom
from article_api.forms.settlement_rules import AddForm, UpdateForm, SelectForm, PermissionForm
from article_api.views_dir.permissions import init_data
import json


# cerf  token验证 用户展示模块
@csrf_exempt
@account.is_token(models.userprofile)
def settlement_rules(request):
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

            # 返回的数据
            ret_data = []

            for obj in objs:

                # 获取选中的id，然后组合成前端能用的数据
                permissionsData = []
                if obj.permissions:
                    permissionsList = [i['id'] for i in obj.permissions.values('id')]
                    if len(permissionsList) > 0:
                        permissionsData = init_data(selected_list=permissionsList)

                #  如果有oper_user字段 等于本身名字
                if obj.oper_user:
                    oper_user_id = obj.oper_user_id
                    oper_user_username = obj.oper_user.username
                else:
                    oper_user_username = ''
                    oper_user_id = ''

                #  将查询出来的数据 加入列表
                ret_data.append({
                    'id': obj.id,
                    'name': obj.name,                           # 角色名称
                    'permissionsData': permissionsData,         # 角色权限
                    'oper_user_id': oper_user_id,               # 操作人ID
                    'oper_user__username': oper_user_username,  # 操作人
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


#  增删改
#  csrf  token验证
@csrf_exempt
@account.is_token(models.userprofile)
def settlement_rules_oper(request, oper_type, o_id):
    response = Response.ResponseObj()
    form_data = {
        'o_id':o_id,
        'oper_user_id': request.GET.get('user_id'),  # 操作人ID
        'reading_num': request.POST.get('reading_num'),  # 阅读数量
        'reading_time': request.POST.get('reading_time'),  # 阅读时长
        'the_amount_of': request.POST.get('the_amount_of'),  # 金额
    }

    forms_obj = PermissionForm(form_data)
    if forms_obj.is_valid():
        success_output_msg("操作结算规则-验证通过")

        if request.method == "POST":

            # 添加结算规则
            if oper_type == "add":
                forms_obj = AddForm(form_data)
                if forms_obj.is_valid():
                    success_output_msg("结算规则添加-验证通过")
                    obj = models.settlement_rules.objects.create(**forms_obj.cleaned_data)
                    response.code = 200
                    response.msg = "添加成功"
                    response.data = {'testCase': obj.id}
                else:
                    error_output_msg("结算规则添加-验证不通过")
                    response.code = 301
                    response.msg = json.loads(forms_obj.errors.as_json())

            # 修改结算规则
            elif oper_type == "update":
                forms_obj = UpdateForm(form_data)
                if forms_obj.is_valid():
                    success_output_msg("修改结算规则-验证通过")

                    o_id, obj = forms_obj.cleaned_data.get('o_id')
                    obj.update(**{
                        'reading_num':forms_obj.cleaned_data.get('reading_num'),
                        'reading_time':forms_obj.cleaned_data.get('reading_time'),
                        'the_amount_of':forms_obj.cleaned_data.get('the_amount_of'),
                        'oper_user_id':forms_obj.cleaned_data.get('oper_user_id'),
                    })
                    response.code = 200
                    response.msg = "修改成功"
                else:
                    error_output_msg("修改结算规则-验证不通过")
                    response.code = 301
                    response.msg = json.loads(forms_obj.errors.as_json())

        else:
            response.code = 402
            response.msg = "请求异常"
    else:
        error_output_msg("操作结算规则-验证不通过")
        response.code = 301
        response.msg = json.loads(forms_obj.errors.as_json())
    return JsonResponse(response.__dict__)
