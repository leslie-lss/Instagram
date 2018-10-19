# -*- coding:utf-8 -*-

import os
import re
import sys
import json
import time
import random
import requests
from hashlib import md5
from pyquery import PyQuery as pq
import cookielib
from pymongo import MongoClient

############################################################################################
#need set
user='hoccgoomusic'
query_hash=''
# cookie = 'sessionid=IGSC7f31ad9f5222e6a51b16b882bb88ef1ed25fb1086562e0dab7fea9e2fb299a61%3AxwZf3SYtiblcnHpFipIMNEzGhDj9QC6r%3A%7B%22_auth_user_id%22%3A6641335349%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%226641335349%3AIH45h0FScI4FCanvGK0qG59khT3B7E55%3Ae91582edfb07c1c7a9cfcbb48bcd45096e3090479a34c66c89650eaee69140fe%22%2C%22last_refreshed%22%3A1539570403.818151474%7D'
referer = 'https://www.instagram.com/' + user + '/'
#设置爬取的时间
start_time = '2011-12-31 23:59:59'
end_time = '2009-01-01 00:00:00'
#存入数据库
def save_mongo(dict):
    conn = MongoClient('192.168.0.50', 27017)
    db = conn.instagram
    my_set = db.hoccgoomusic_1019
    try:
        my_set.insert(dict)
        print('******************insert database success!*************************')
    except:
        print('###################insert database fail!!#######################')
############################################################################################
start_time_array = time.strptime(start_time, '%Y-%m-%d %H:%M:%S')
start_time = time.mktime(start_time_array)
end_time_array = time.strptime(end_time, '%Y-%m-%d %H:%M:%S')
end_time = time.mktime(end_time_array)

url_base = 'https://www.instagram.com/'
uri = 'https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{cursor}%22%7D'
my_headers = [    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
                  "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                  'Opera/9.25 (Windows NT 5.1; U; en)',
                  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                  'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                  'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                  "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                  "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36']

my_proxies = {
        'http': 'http://127.0.0.1:1080',
        'https': 'https://127.0.0.1:1080'
    }   # 本机代理接口

headers = {
    'user-agent': my_headers[0]
}
headers_json = {
    'user-agent': my_headers[0],
    'cookie': cookie,
    'referer': referer
}

def refresh_cookie():
    #创建MozillaCookieJar实例对象
    cookie = cookielib.MozillaCookieJar()
    #从文件中读取cookie内容到变量
    cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    return cookie

def get_html(url):
    try:
        response = requests.get(url, headers=headers, cookies=refresh_cookie())
        if response.status_code == 200:
            return response.text
        else:
            print('请求网页源代码错误, 错误状态码:', response.status_code)
    except Exception as e:
        print(e)
        return None


def get_json(url):
    try:
        response = requests.get(url, headers=headers_json, proxies=my_proxies, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print('请求网页json wrong错误, 错误状态码:', response.status_code)
    except Exception as e:
        print(e)
        time.sleep(60 + float(random.randint(1, 4000))/100)
        return get_json(url)

def get_data(edges):

    for edge in edges:
        dict = {}
        dict['media_url'] = []

        if edge['node']['taken_at_timestamp'] > start_time:
            continue
        if edge['node']['taken_at_timestamp'] < end_time:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@success!!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            sys.exit(0)


        if edge['node']['shortcode']:
            dict['shortcode'] = edge['node']['shortcode'].encode('utf-8')
            dict['url'] = 'https://www.instagram.com/p/'+dict['shortcode']+'/?taken-by=' + user
        if edge['node']['taken_at_timestamp']:
            dict['taken_at_timestamp'] = edge['node']['taken_at_timestamp']
        if edge['node']['__typename']:
            dict['typename'] = edge['node']['__typename'].encode('utf-8')
        if edge['node']['edge_media_to_comment']['count']:
            dict['comment_count'] = edge['node']['edge_media_to_comment']['count']
        if edge['node']['edge_media_preview_like']['count']:
            dict['like_count'] = edge['node']['edge_media_preview_like']['count']
        try:
            if edge['node']['edge_media_to_caption']['edges'][0]['node']['text']:
                print edge['node']['edge_media_to_caption']['edges'][0]['node']['text']
                dict['text'] = edge['node']['edge_media_to_caption']['edges'][0]['node']['text'].encode('utf-8')
        except:
            dict['text'] = ''
        if edge['node']['__typename'] == 'GraphSidecar':
            edge_edges = edge['node']['edge_sidecar_to_children']['edges']
            for edge_edge in edge_edges:
                if edge_edge['node']['is_video']:
                    video_url = edge_edge['node']['video_url'].encode('utf-8')
                    if video_url:
                        dict['media_url'].append(video_url)
                else:
                    display_url = edge_edge['node']['display_url'].encode('utf-8')
                    if display_url:
                        dict['media_url'].append(display_url)
        else:
            if edge['node']['is_video']:
                video_url = edge['node']['video_url'].encode('utf-8')
                if video_url:
                    dict['media_url'].append(video_url)
            else:
                display_url = edge['node']['display_url'].encode('utf-8')
                if display_url:
                    dict['media_url'].append(display_url)
        save(dict)
        save_mongo(dict)
        print('-----------------------------------------------------------')
        time.sleep(1)
    return dict



def get_content(url):
    try:
        response = requests.get(url, headers=headers, cookies=refresh_cookie(), timeout=10)
        if response.status_code == 200:
            return response.content
        else:
            print('请求照片二进制流错误, 错误状态码:', response.status_code)
    except Exception as e:
        print(e)
        return None

def save(dict):
    dirpath = r'D:\python\Instagram_crawler-master\Instagram_crawler-master\Instagram\{0}'.format(user)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    dict_urls = dict['media_url']

    print dict_urls

    time_local = time.localtime(dict['taken_at_timestamp'])
    month = time.strftime('%Y_%m', time_local)
    post_time = time.strftime('%Y-%m-%d_%H%M%S',time_local)
    dirpath = r'D:\python\Instagram_crawler-master\Instagram_crawler-master\Instagram\{0}\{1}'.format(user, user + '_' + month)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)

    dirpath = r'D:\python\Instagram_crawler-master\Instagram_crawler-master\Instagram\{0}\{1}\{2}'.format(user, user + '_' + str(month), str(post_time))
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    detail_path = r'D:\python\Instagram_crawler-master\Instagram_crawler-master\Instagram\{0}\{1}\{2}\{3}'.format(
        user, user + '_' + str(month), str(post_time), 'detail.txt')
    if not os.path.exists(detail_path):
        with open(detail_path, 'w') as f:
            detail = ["发帖时间：" + str(post_time) + '\n' ,
                      "点赞数：" + str(dict['like_count']) + '\n' ,
                      "评论数：" + str(dict['comment_count']) + '\n' ,
                      "帖子内容：\n\n" + dict['text'] + '\n\n' ,
                      "帖子链接：" + dict['url']]
            f.writelines(detail)
            f.close()
    for i in range(len(dict_urls)):
        try:
            content = get_content(dict_urls[i])
            medianame = 'p' + str(i) + '.' + dict_urls[i][-3:]
            file_path = r'D:\python\Instagram_crawler-master\Instagram_crawler-master\Instagram\{0}\{1}\{2}\{3}'.format(
                user, user + '_' + str(month), str(post_time), medianame)
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    print('正在下载第{0}张:'.format(i) + dict_urls[i], ' 还剩{0}张'.format(len(dict_urls) - i - 1))
                    f.write(content)
                    f.close()
            else:
                print('第{0}张照片已下载'.format(i))
        except Exception as e:
            print(e)
            print('这张图片or视频下载失败')
            print(dict['taken_at_timestamp'])
            sys.exit(0)




def get_urls(html):
    user_id = re.findall('"profilePage_([0-9]+)"', html, re.S)[0]
    print('user_id:' + user_id)
    doc = pq(html)
    items = doc('script[type="text/javascript"]').items()
    for item in items:
        if item.text().strip().startswith('window._sharedData'):
            js_data = json.loads(item.text()[21:-1], encoding='utf-8')
            edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
            page_info = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]['page_info']
            cursor = page_info['end_cursor']
            flag = page_info['has_next_page']
            print(cursor, flag)
    while flag:
        url = uri.format(query_hash=query_hash, user_id=user_id, cursor=cursor)
        js_data = get_json(url)
        try:
            edges = js_data['data']['user']['edge_owner_to_timeline_media']['edges']
            cursor = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            flag = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
            dict = get_data(edges)
        except:
            print(js_data)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            time.sleep(30)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            try:
                time.sleep(30)
                url = uri.format(query_hash=query_hash, user_id=user_id, cursor=cursor)
                js_data = get_json(url)
                time.sleep(30)
                edges = js_data['data']['user']['edge_owner_to_timeline_media']['edges']
                cursor = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
                flag = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
                dict = get_data(edges)
            except:
                print(js_data)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                sys.exit(0)


def main(user):
    url = url_base + user + '/'
    html = get_html(url)
    urls = get_urls(html)
    

if __name__ == '__main__':
    user_name = user
    start = time.time()
    main(user_name)
    print('Complete!!!!!!!!!!')
    end = time.time()
    spend = end - start
    hour = spend // 3600
    minu = (spend - 3600 * hour) // 60
    sec = spend - 3600 * hour - 60 * minu
    #print(f'一共花费了{hour}小时{minu}分钟{sec}秒')
