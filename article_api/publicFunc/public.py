from django.db.models import Q
from article_api import models
import datetime

# 记录用户最后登录时间
def record_user_last_login_time(user_id):
    now = datetime.datetime.today()
    objs = models.userprofile.objects.filter(id=user_id)
    objs.update(last_login_time=now)


# 分组树状图
def GroupTree(parent_class_id=None):
    result_data = []
    q = Q()
    q.add(Q(parent_class_id=parent_class_id), Q.AND)
    objs = models.classfiy.objects.filter(q)
    for obj in objs:
        current_data = {
            'id': obj.id,
            'classify_name':obj.classify_name,
            'expand': False,
            'checked': False,
        }
        children_data = GroupTree(obj.id)
        current_data['children'] = children_data
        result_data.append(current_data)

    return result_data


# 修改分类 判断是否死循环
def UpdateClassfiyGroupTree(o_id, parent_class_id):
    flag = False
    q = Q()
    q.add(Q(id=parent_class_id), Q.AND)
    objs = models.classfiy.objects.filter(q)
    for obj in objs:
        if obj.parent_class:
            if int(obj.parent_class_id) == int(o_id):
                return True

            else:
                flag = UpdateClassfiyGroupTree(o_id, obj.parent_class_id)
        else:
            return False
    return flag