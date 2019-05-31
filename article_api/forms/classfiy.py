from django import forms

from article_api import models
from article_api.publicFunc import public
from article_api.publicFunc.public import judgment_classification_level

# 添加
class AddForm(forms.Form):
    classify_name = forms.CharField(
        required=True,
        error_messages={
            'required': "分类名不能为空"
        }
    )
    oper_user_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '操作人不能为空'
        }
    )

    parent_class = forms.IntegerField(
        required=False,
        error_messages={
            'required': "父级权限类型错误"
        }
    )

    # # 查询名称是否存在
    # def clean_classify_name(self):
    #     classify_name = self.data.get('classify_name')
    #     objs = models.classfiy.objects.filter(
    #         classify_name=classify_name,
    #     )
    #     if objs:
    #         self.add_error('classify_name', '分类名称已存在')
    #     else:
    #         return classify_name

    def clean_parent_class(self):
        parent_class = self.data.get('parent_class')
        if parent_class:
            parent_class_objs = models.classfiy.objects.filter(id=parent_class)
            if parent_class_objs:
                classifiy_level = judgment_classification_level(parent_class, num=0) # 判断父级分类等级

                if classifiy_level <= 2:
                    classifiy_level += 1   # 当前添加的分类等级
                    return parent_class, classifiy_level
                else:
                    self.add_error('parent_class', '分类超过三级')
            else:
                self.add_error('parent_class', '父级分类不存在')

# 更新
class UpdateForm(forms.Form):
    o_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': "修改分类不能为空"
        }
    )
    classify_name = forms.CharField(
        required=True,
        error_messages={
            'required': "分类名不能为空"
        }
    )
    oper_user_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '操作人不能为空'
        }
    )

    parent_class = forms.IntegerField(
        required=False,
        error_messages={
            'required': "父级权限类型错误"
        }
    )

    # 查询名称是否存在
    def clean_classify_name(self):
        classify_name = self.data.get('classify_name')
        o_id = self.data.get('o_id')
        objs = models.classfiy.objects.filter(
            classify_name=classify_name,
        ).exclude(id=o_id)
        if objs:
            self.add_error('classify_name', '分类名称已存在')
        else:
            return classify_name

    def clean_parent_class(self):
        parent_class = self.data.get('parent_class')
        if parent_class:
            parent_class_objs = models.classfiy.objects.filter(id=parent_class)
            if parent_class_objs:

                classifiy_level = judgment_classification_level(parent_class, num=0)  # 判断父级分类等级

                if classifiy_level <= 2:
                    classifiy_level += 1  # 当前添加的分类等级
                    return parent_class, classifiy_level

                else:
                    self.add_error('parent_class', '分类超过三级')
            else:
                self.add_error('parent_class', '父级分类不存在')

    def clean_o_id(self):
        o_id = self.data.get('o_id')
        parent_class = self.data.get('parent_class')
        if o_id != parent_class:
            objs = models.classfiy.objects.filter(id=o_id)
            if objs:

                flag = public.UpdateClassfiyGroupTree(o_id)
                if parent_class:
                    flag = public.UpdateClassfiyGroupTree(o_id, parent_class)

                if flag:
                    self.add_error('o_id', '不能放在此分类下')

                else:
                    return o_id, objs

            else:
                self.add_error('o_id', '修改分类不存在')
        else:
            self.add_error('o_id', '父级不能设置为自己')

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

    def clean_user_id(self):
        user_id = self.data.get('user_id')
        objs = models.userprofile.objects.filter(id=user_id)
        if not objs or objs[0].status == 2:
            self.add_error('user_id', '非法用户')
        else:
            return user_id

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