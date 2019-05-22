from django.db.models import Q
from article_api import models
import datetime, re

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
def UpdateClassfiyGroupTree(o_id, parent_class_id=None):
    flag = False
    q = Q()
    q.add(Q(id=parent_class_id), Q.AND)
    print('q-----------> ', q)
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




# 数据统计 查询 该分类下所有文章
def data_statistics_get_article(num, o_id):
    objs = models.classfiy.objects.filter(parent_class_id=o_id)
    for obj in objs:
        article_count = models.article.objects.filter(classfiy=obj.id).count()
        num += article_count
        data_statistics_get_article(obj.id, num)
        # article_list = []
        # for article_obj in article_objs:
        #     article_list.append({
        #
        #     })
        #
        # current_data = {
        #     'class_id': obj.id,
        #     'article_list': article_list,
        #     'expand': False,
        #     'checked': False,
        # }
    #     current_data['children'] = children_data
    #     result_data.append(current_data)
    return num




# 时间筛选
def time_screen(number_days):
    now_datetime = datetime.datetime.today()

    data = []
    if number_days == 'today':  # 今天
        ymd = datetime.datetime.strftime(now_datetime, '%Y-%m-%d')
        data.append({
            'ymd': ymd,
            'start_time': ymd + ' 00:00:00',
            'stop_time': ymd + ' 23:59:59'
        })

    else:
        if number_days == 'seven_days':  # 近七天
            days = 7
        elif number_days == 'thirty_days':  # 近三十天
            days = 30
        else:  # 默认昨天
            # if number_days == 'yesterday':  # 昨天
            days = 1

        for day in range(days):
            day += 1
            specify_time = now_datetime - datetime.timedelta(days=day)
            ymd = datetime.datetime.strftime((specify_time), '%Y-%m-%d')
            start_time = ymd + ' 00:00:00'
            stop_time = ymd + ' 23:59:59'
            data.append({
                'ymd': ymd,
                'start_time': start_time,
                'stop_time': stop_time
            })


    return data


def verify_mobile_phone_number(phone):
    flag = False
    phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
    res = re.search(phone_pat, phone)
    if res:
        flag = True

    return flag










