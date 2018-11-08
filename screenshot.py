#coding:utf-8

# -*- coding:utf-8 -*-
import sys
import time
import redis
import cookielib
from pymongo import MongoClient
from selenium import webdriver
import os


user='hoccgoomusic'

service_args = [
    '--proxy=https://127.0.0.1:1080',
    '--proxy-type=https',
]

def get_url(url_list):
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.instagram
    my_set = db.hoccgoomusic_1108

    while r.llen(url_list) > 0:
        print("-------------------------------------------------------------------------------")
        url = r.lpop(url_list)
        print(url)
        dict = my_set.find_one({'url': url})
        time_local = time.localtime(dict['taken_at_timestamp'])
        month = time.strftime('%Y_%m', time_local)
        post_time = time.strftime('%Y-%m-%d_%H%M%S', time_local)
        dirpath = r'D:\python\Instagram_crawler-master\Instagram_crawler-master\Instagram\screenshot\{0}\{1}'.format(user, str(month))
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        pic_name = str(post_time)
        imageName = pic_name + '.png'
        pic_path = r'D:\python\Instagram_crawler-master\Instagram_crawler-master\Instagram\screenshot\{0}\{1}\{2}'.format(user, str(month), imageName)
        if os.path.exists(pic_path):
            continue
        myDriver = webdriver.PhantomJS(r'D:\python\phantomjs-2.1.1-windows\bin\phantomjs.exe',service_args=service_args)
        get_picture(myDriver, url, pic_path)
        myDriver.quit()

#得到有效链接的截图
def get_picture(myDriver, url, fpath):
    retry = 5
    while retry > 0:
        try:
            myDriver.set_page_load_timeout(15)#设置网页加载超时时间为10秒
            myDriver.get(url)
            myDriver.get_screenshot_as_file(fpath)#截取网页内容，已当前时间戳为图片命名保存
            myDriver.close()
            retry = 0
        except:
            s= u'当前网页超时：%s\n' %url
            print s
            time.sleep(5)
            retry = retry - 1
            if retry == 0:
                pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
                r = redis.Redis(connection_pool=pool)
                r.rpush(url_list, url)
                print("%%%%%%%%%%%%")

if __name__ == '__main__':
    url_list = 'url'
    get_url(url_list)