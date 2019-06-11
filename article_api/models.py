from django.db import models

# Create your models here.


from django.db import models




# 权限表
class permissions(models.Model):
    name = models.CharField(verbose_name="权限名称", max_length=128)
    title = models.CharField(verbose_name="权限标题", max_length=128)
    pid = models.ForeignKey('self', verbose_name="父级权限", null=True, blank=True)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    oper_user = models.ForeignKey('userprofile', verbose_name="创建用户", related_name='permissions_user', null=True, blank=True)


# 角色表
class role(models.Model):
    name = models.CharField(verbose_name="角色名称", max_length=128)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    oper_user = models.ForeignKey('userprofile', verbose_name="创建用户", related_name='role_user', null=True, blank=True)
    permissions = models.ManyToManyField('permissions', verbose_name="拥有权限")

# 用户表
class userprofile(models.Model):
    username = models.CharField(verbose_name="用户账号", max_length=128)
    password = models.CharField(verbose_name="用户密码", max_length=128)
    token = models.CharField(verbose_name="token值", max_length=128)
    oper_user = models.ForeignKey('userprofile', verbose_name="创建用户", related_name='hzxy_userprofile_create_date', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    status_choices = (
        (1, '已审核'),
        (2, '未审核'),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)

    last_login_time = models.DateTimeField(verbose_name='最后登录时间', null=True)
    role = models.ForeignKey('role', verbose_name='所属角色', null=True)
    # set_avator = models.CharField(verbose_name='头像', default='http://api.zhugeyingxiao.com/statics/imgs/setAvator.jpg', max_length=128)
    phone = models.CharField(verbose_name='电话', max_length=16, null=True, blank=True)
    the_amount_of = models.IntegerField(verbose_name='金额(元)', default=0)

# 文章类别
class classfiy(models.Model):
    oper_user = models.ForeignKey('userprofile', verbose_name="创建用户", null=True, blank=True)
    parent_class = models.ForeignKey('self', verbose_name='父级分类', null=True, blank=True)
    classify_name = models.CharField(verbose_name='分类名称', max_length=64, null=True, blank=True)
    number_articles = models.IntegerField(verbose_name='该分类下存在文章个数', default=0)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    level = models.IntegerField(verbose_name='分类等级', default=1)

# 文章表
class article(models.Model):
    belongToUser = models.ForeignKey('userprofile', verbose_name='文章(属于/谁/创建)', null=True, related_name='belongToUser_userprofile')
    title = models.CharField(verbose_name='文章标题', max_length=128)
    summary = models.TextField(verbose_name='文章摘要', null=True, blank=True)
    content = models.TextField(verbose_name='文章内容', null=True, blank=True)
    style = models.TextField(verbose_name='文章样式', null=True, blank=True)
    article_cover = models.CharField(verbose_name='文章封面图片', max_length=128, null=True, blank=True)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    is_delete = models.IntegerField(verbose_name='逻辑删除', default=0)

    article_source_choices = (
        (1, '添加'),
        (2, '转载'),
    )
    article_source = models.SmallIntegerField(verbose_name='文章来源', choices=article_source_choices, default=1)
    edit_name = models.CharField(verbose_name='编辑名称', max_length=16)
    classfiy = models.ForeignKey('classfiy', verbose_name='类别')
    article_word_count = models.IntegerField(verbose_name='文章字数', null=True)
    original_link = models.TextField(verbose_name='原文链接(仅限article_source=2)', null=True)

    # is_send = models.IntegerField(verbose_name='是否上传', default=0)
    # stop_upload = models.IntegerField(verbose_name='停止/恢复上传', default=0)

# 计费结算日志
class billing_log(models.Model):
    article = models.ForeignKey(to='article', verbose_name='归属文章')
    price_num = models.CharField(verbose_name='拨出费用', max_length=128, null=True, blank=True)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

# 结算规则表
# class settlement_rules(models.Model):
#     reading_num = models.IntegerField(verbose_name='阅读量', default=0)
#     reading_time = models.IntegerField(verbose_name='阅读时长(S)', default=0)
#     the_amount_of = models.IntegerField(verbose_name='金额(元)', default=0)
#     oper_user = models.ForeignKey('userprofile', verbose_name='操作人', null=True, related_name='oper_user_userprofile')




















