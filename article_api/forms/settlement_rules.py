from django import forms

from article_api import models
import json


# 添加
class AddForm(forms.Form):
    oper_user_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': "亲, 请登录!"
        }
    )
    reading_num = forms.IntegerField(
        required=False,
        error_messages={
            'required': "亲, 阅读数量只能写数字哦~"
        }
    )
    reading_time = forms.IntegerField(
        required=False,
        error_messages={
            'required': "亲, 阅读时长规则、只能写数字哦~"
        }
    )
    the_amount_of = forms.IntegerField(
        required=True,
        error_messages={
            'required': "亲, 金额不能为空哦~"
        }
    )

    # 操作人验证
    def clean_oper_user_id(self):
        oper_user_id = self.data.get('oper_user_id')
        if models.userprofile.objects.filter(id=oper_user_id):
            if models.settlement_rules.objects.all():
                self.add_error('oper_user_id', '亲, 已有规则 不能添加咯~')
            else:
                return oper_user_id
        else:
            self.add_error('oper_user_id', '非法用户')

# 更新
class UpdateForm(forms.Form):
    o_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '没有修改的数据'
        }
    )

    oper_user_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': "亲, 请登录!"
        }
    )
    reading_num = forms.IntegerField(
        required=False,
        error_messages={
            'required': "亲, 阅读数量只能写数字哦~"
        }
    )
    reading_time = forms.IntegerField(
        required=False,
        error_messages={
            'required': "亲, 阅读时长规则、只能写数字哦~"
        }
    )
    the_amount_of = forms.IntegerField(
        required=True,
        error_messages={
            'required': "亲, 金额不能为空哦~"
        }
    )

    # 操作人验证
    def clean_oper_user_id(self):
        oper_user_id = self.data.get('oper_user_id')
        if models.userprofile.objects.filter(id=oper_user_id):
            return oper_user_id
        else:
            self.add_error('oper_user_id', '非法用户')

    # 修改ID验证
    def clean_o_id(self):
        o_id = self.data.get('o_id')
        obj = models.settlement_rules.objects.filter(id=o_id)
        if obj:
            return o_id, obj
        else:
            self.add_error('o_id', '亲, 数据丢了~')


# 判断是否是数字
class SelectForm(forms.Form):
    current_page = forms.IntegerField(
        required=False,
        error_messages={
            'required': "页码数据类型错误"
        }
    )

    length = forms.IntegerField(
        required=False,
        error_messages={
            'required': "页显示数量类型错误"
        }
    )

    user_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': "非法用户"
        }
    )

    def clean_current_page(self):
        if 'current_page' not in self.data:
            current_page = 1
        else:
            current_page = int(self.data['current_page'])
        return current_page

    def clean_length(self):
        if 'length' not in self.data:
            length = 10
        else:
            length = int(self.data['length'])
        return length

# 验证权限
class PermissionForm(forms.Form):

    oper_user_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': "亲, 请先登录~"
        }
    )

    # 操作人验证
    def clean_oper_user_id(self):
        oper_user_id = self.data.get('oper_user_id')
        objs = models.userprofile.objects.filter(id=oper_user_id)
        if objs:
            if int(objs[0].role_id) == 1:
                return oper_user_id
            else:
                self.add_error('oper_user_id', '亲, 木有权限')
        else:
            self.add_error('oper_user_id', '非法用户')



