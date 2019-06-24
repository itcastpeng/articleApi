from django import forms

from article_api import models
import json
from article_api.publicFunc.public import Classification_judgment

# 添加
class AddForm(forms.Form):
    title = forms.CharField(
        required=True,
        error_messages={
            'required': "文章标题不能为空"
        }
    )
    summary = forms.CharField(
        required=True,
        error_messages={
            'required': '文章摘要不能为空'
        }
    )

    content = forms.CharField(
        required=True,
        error_messages={
            'required': "文章内容不能为空"
        }
    )

    article_cover = forms.CharField(
        required=True,
        error_messages={
            'required': "文章图片不能为空"
        }
    )
    belongToUser_id = forms.CharField(
        required=True,
        error_messages={
            'required': "亲, 请登录!"
        }
    )
    article_source = forms.IntegerField(
        required=True,
        error_messages={
            'required': "亲, 选择文章来源!"
        }
    )
    edit_name = forms.CharField(
        required=True,
        error_messages={
            'required': "亲, 请写文章编辑人别名!"
        }
    )
    article_word_count= forms.IntegerField(
        required=True,
        error_messages={
            'required': "文章字数不能为空"
        }
    )
    classfiy_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': "分类不能为空"
        }
    )
    toward_whether = forms.IntegerField(
        required=True,
        error_messages={
            'required': "是否对外不能为空"
        }
    )

    def clean_classfiy_id(self):
        classfiy_id = self.data.get('classfiy_id')
        flag = Classification_judgment(classfiy_id)
        if flag:
            self.add_error('classfiy_id', '请选择三级分类')
        else:
            return classfiy_id

    # 查询名称是否存在
    def clean_title(self):
        title = self.data['title']
        objs = models.article.objects.filter(
            title=title,
        )
        if objs:
            self.add_error('title', '亲, 文章标题被占用啦!')
        else:
            return title

    # 操作人验证
    def clean_belongToUser_id(self):
        belongToUser_id = self.data.get('belongToUser_id')
        if models.userprofile.objects.filter(id=belongToUser_id):
            return belongToUser_id
        else:
            self.add_error('belongToUser_id', '非法用户')


# 更新
class UpdateForm(forms.Form):
    o_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '角色id不能为空'
        }
    )

    title = forms.CharField(
        required=True,
        error_messages={
            'required': "文章标题不能为空"
        }
    )
    classfiy_id = forms.CharField(
        required=True,
        error_messages={
            'required': "分类不能为空"
        }
    )
    summary = forms.CharField(
        required=False,
        error_messages={
            'required': '文章摘要类型错误'
        }
    )

    content = forms.CharField(
        required=True,
        error_messages={
            'required': "文章内容不能为空"
        }
    )

    article_cover = forms.CharField(
        required=True,
        error_messages={
            'required': "文章图片不能为空"
        }
    )
    belongToUser_id = forms.CharField(
        required=True,
        error_messages={
            'required': "亲, 请登录!"
        }
    )
    article_source = forms.IntegerField(
        required=True,
        error_messages={
            'required': "亲, 选择文章来源!"
        }
    )
    edit_name = forms.CharField(
        required=False,
        error_messages={
            'required': "编辑人别名类型错误"
        }
    )
    article_word_count = forms.IntegerField(
        required=True,
        error_messages={
            'required': "文章字数不能为空"
        }
    )
    toward_whether = forms.IntegerField(
        required=True,
        error_messages={
            'required': "是否对外不能为空"
        }
    )

    # 查询名称是否存在
    def clean_title(self):
        title = self.data.get('title')
        o_id = self.data.get('o_id')
        objs = models.article.objects.filter(
            title=title,
        ).exclude(id=o_id)
        if objs:
            self.add_error('title', '亲, 文章标题被占用啦!')
        else:
            return title

    # 操作人
    def clean_belongToUser_id(self):
        belongToUser_id = self.data.get('belongToUser_id')
        if models.userprofile.objects.filter(id=belongToUser_id):
            return belongToUser_id
        else:
            self.add_error('belongToUser_id', '非法用户')

    # 修改ID验证
    def clean_o_id(self):
        o_id = self.data.get('o_id')
        obj = models.article.objects.filter(id=o_id)
        if obj:
            # if int(obj[0].is_send) != 0:
            #     self.add_error('o_id', '该文章已上传, 如有疑问请联系管理员')
            # else:
            return o_id, obj
        else:
            self.add_error('o_id', '亲, 数据丢了~')

    def clean_classfiy_id(self):
        classfiy_id = self.data.get('classfiy_id')
        flag = Classification_judgment(classfiy_id)
        if flag:
            self.add_error('classfiy_id', '请选择三级分类')
        else:
            return classfiy_id

# 删除
class DeleteForm(forms.Form):
    o_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '角色id不能为空'
        }
    )

    belongToUser_id = forms.CharField(
        required=True,
        error_messages={
            'required': "亲, 请登录!"
        }
    )

    # 操作人验证
    def clean_belongToUser_id(self):
        belongToUser_id = self.data.get('belongToUser_id')
        if models.userprofile.objects.filter(id=belongToUser_id):
            return belongToUser_id
        else:
            self.add_error('belongToUser_id', '非法用户')

    # 验证文章ID
    # def clean_o_id(self):
    #     o_id = self.data.get('o_id')
    #     belongToUser_id = self.data.get('belongToUser_id')
    #     obj = models.article.objects.filter(id=o_id, belongToUser_id=belongToUser_id)
    #     if not obj:
    #         self.add_error('o_id', '亲, 您不能删除这个文章!')
    #     else:
    #         if int(obj[0].is_send) == 0:
    #             return o_id, obj
    #         else:
    #             self.add_error('o_id', '该文章已上传, 如有疑问请联系管理员')



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

# 转载文章
class AddRepostsForm(forms.Form):
    reprint_link = forms.CharField(
        required=True,
        error_messages={
            'required': "转载的链接不能为空"
        }
    )
    classfiy_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': "分类类别不能为空"
        }
    )
    edit_name = forms.CharField(
        required=True,
        error_messages={
            'required': "编辑名称不能为空"
        }
    )
    toward_whether = forms.IntegerField(
        required=True,
        error_messages={
            'required': "是否对外不能为空"
        }
    )

    def clean_classfiy_id(self):
        classfiy_id = self.data.get('classfiy_id')
        objs = models.classfiy.objects.filter(id=classfiy_id)
        if objs:
            obj = objs[0]
            if obj.level == 3:
                return classfiy_id
            else:
                self.add_error('classfiy_id', '请选取三级分类')
        else:
            self.add_error('classfiy_id', '该分类不存在')









