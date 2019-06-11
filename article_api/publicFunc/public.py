from django.db.models import Q
from article_api import models
from bs4 import BeautifulSoup
from article_api.publicFunc.account import randon_str
from urllib.parse import unquote
import datetime, re, requests, random, time, os, sys

URL = 'http://wenzhangku.zhugeyingxiao.com/api/'
pub_statics_url = os.path.join('statics', 'img')  # 公共文件夹


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

# 下载视频到本地
def requests_video_download(url):
    img_save_path = pub_statics_url + randon_str() + '.mp4'
    r = requests.get(url, stream=True)
    with open(img_save_path, "wb") as mp4:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                mp4.write(chunk)

    return URL + img_save_path

# 下载微信图片 到本地 并返回新连接
def download_img(img_content, headers):
    randon_str_obj = randon_str()
    if 'wx_fmt=gif' in img_content:
        img_name = "/{}.gif".format(randon_str_obj)
    else:
        img_name = "/{}.jpg".format(randon_str_obj)
    path = pub_statics_url + img_name
    ret = requests.get(img_content, headers=headers)
    with open(path, 'wb') as file:
        file.write(ret.content)
    return URL + path


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

    cover_url = download_img(cover_url, headers) # 下载封面

    # 获取所有样式
    style = ""
    style_tags = soup.find_all('style')
    for style_tag in style_tags:
        style += str(style_tag)

    # 获取所有图片
    body = soup.find('div', id="js_content")
    body.attrs['style'] = "padding: 20px 16px 12px;"
    img_tags = soup.find_all('img')
    for img_tag in img_tags:
        data_src = img_tag.attrs.get('data-src')
        if data_src:
            if img_tag.attrs.get('style'):
                img_tag.attrs['style'] = img_tag.attrs.get('style')

            img_url = download_img(data_src, headers)
            img_tag.attrs['data-src'] = img_url

    ## 处理视频的URL
    iframe = body.find_all('iframe', attrs={'class': 'video_iframe'})
    for iframe_tag in iframe:
        shipin_url = iframe_tag.get('data-src')
        data_cover_url = iframe_tag.get('data-cover')  # 封面
        if data_cover_url:
            data_cover_url = unquote(data_cover_url, 'utf-8')
            data_cover_url = download_img(data_cover_url, headers) # 视频封面

        vid = shipin_url.split('vid=')[1]
        if 'wxv' in vid:  # 下载
            iframe_url = 'https://mp.weixin.qq.com/mp/videoplayer?vid={}&action=get_mp_video_play_url'.format(vid)
            ret = requests.get(iframe_url)
            url = ret.json().get('url_info')[0].get('url')
            img_save_path = requests_video_download(url)
            iframe_tag_new = """<div style="width: 100%; background: #000; position:relative; height: 0; padding-bottom:75%;">
                                                <video style="width: 100%; height: 100%; position:absolute;left:0;top:0;" id="videoBox" src="{}" poster="{}" controls="controls" allowfullscreen=""></video>
                                            </div>""".format(img_save_path, data_cover_url)

        else:
            if '&' in shipin_url and 'vid=' in shipin_url:
                _url = shipin_url.split('?')[0]
                shipin_url = _url + '?vid=' + vid
            if vid:
                shipin_url = 'https://v.qq.com/txp/iframe/player.html?origin=https%3A%2F%2Fmp.weixin.qq.com&vid={}&autoplay=false&full=true&show1080p=false&isDebugIframe=false'.format(
                    vid
                )
            iframe_tag.attrs['data-src'] = shipin_url
            iframe_tag.attrs['allowfullscreen'] = True  # 是否允许全屏
            iframe_tag.attrs['data-cover'] = data_cover_url

            iframe_tag_new = str(iframe_tag).replace('></iframe>', ' width="100%" height="500px"></iframe>')
        body = str(body).replace(str(iframe_tag), iframe_tag_new)
        body = BeautifulSoup(body, 'html.parser')

    content = str(style) + str(body) # 相加 样式 和 内容
    dict = {'url': '', 'data-src': 'src', '?wx_fmt=jpg': '', '?wx_fmt=png': '', '?wx_fmt=jpeg': '',
            '?wx_fmt=gif': '', }  # wx_fmt=gif
    for key, value in dict.items(): # 替换带有 mmbiz.qpic.cn 的链接 和微信识别的后缀
        if key == 'url':
            pattern1 = re.compile(r'https:\/\/mmbiz.qpic.cn\/\w+\/\w+\/\w+\?\w+=\w+', re.I)  # 通过 re.compile 获得一个正则表达式对象
            pattern2 = re.compile(r'https:\/\/mmbiz.qpic.cn\/\w+\/\w+\/\w+', re.I)
            results_url_list_1 = pattern1.findall(content)
            results_url_list_2 = pattern2.findall(content)
            results_url_list_1.extend(results_url_list_2)
            for pattern_url in results_url_list_1:
                file_dir = download_img(pattern_url, headers)
                sub_url = 'http://statics.api.zhugeyingxiao.com/' + file_dir
                content = content.replace(pattern_url, sub_url)
        else:
            content = content.replace(key, value)

    result_data = {
        'original_link': reprint_link,
        'title': title,
        'summary': summary,
        'article_cover': cover_url,
        'style': style,
        'content': content,
    }

    return result_data


