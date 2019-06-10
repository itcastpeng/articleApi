from django.db.models import Q
from article_api import models
from bs4 import BeautifulSoup
from article_api.publicFunc.base64_encryption import b64decode, b64encode
import datetime, re, requests, random

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

# 验证手机号
def verify_mobile_phone_number(phone):
    flag = False
    phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
    res = re.search(phone_pat, phone)
    if res:
        flag = True

    return flag

# 判断分类 级别
def judgment_classification_level(parent, num):
    # print('num----============> ', num)
    objs = models.classfiy.objects.filter(id=parent)
    if objs:
        num += 1
        num = judgment_classification_level(objs[0].parent_class_id, num)

    return num

# 添加修改文章 判断选择的分类 是否为最低级
def Classification_judgment(classify_list):
    objs = models.classfiy.objects.filter(id=classify_list)
    flag = False
    for obj in objs:
        if obj.level != 3:
            flag = True
            break
    return flag

# 查询 分类所有上级
def query_classification_supervisor(classify_id, class_list):
    obj = models.classfiy.objects.get(id=classify_id)
    print('obj.parent_class_id------------>', obj.parent_class_id)
    if obj.parent_class_id:
        class_list.append({
            'level':obj.level,
            'id':obj.id
        })
        class_list = query_classification_supervisor(obj.parent_class_id, class_list)
    else:
        class_list.append({
            'level': obj.level,
            'id': obj.id
        })
    return class_list


# 获取微信文章
def get_content(reprint_link):

    pcRequestHeader = [
        'Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.16) Gecko/20101130 Firefox/3.5.16',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; .NET CLR 1.1.4322)',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2; zh-CN; rv:1.9.0.19) Gecko/2010031422 Firefox/3.0.19 (.NET CLR 3.5.30729)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13'
    ]
    headers = {'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)]}
    ret = requests.get(reprint_link, headers=headers)
    title = re.compile(r'var msg_title = (.*);').findall(ret.text)[0].replace('"', '')  # 标题
    summary = re.compile(r'var msg_desc = (.*);').findall(ret.text)[0].replace('"', '')  # 摘要
    cover_url = re.compile(r'var msg_cdn_url = (.*);').findall(ret.text)[0].replace('"', '')  # 封面

    soup = BeautifulSoup(ret.text, 'lxml')


    # 获取所有样式
    style = ""
    style_tags = soup.find_all('style')
    for style_tag in style_tags:
        style += str(style_tag)





















