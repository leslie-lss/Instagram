# Instagram
爬取Instagram上某一账户的全部post，包括正文，点赞数，评论数，发帖时间，帖子链接，并且下载相应的图片或视频

## need set
需要填写user的名字

利用getCookie.py获取cookie备用

在instagram的用户主页按下F12，获取对应的query_hash以及cookie中的sessionid

此爬虫还将数据信息存储进入mongodb中，可以选择

## 爬虫结构

爬虫程序大致运行顺序及意义：

>get_html()：获取到首页源码

>get_urls()：获取到动态加载的ajax页面信息

>get_json()：获取到动态加载的帖子的json数据

>get_data()：解析获取到的json数据

>save()：保存相应的帖子信息，下载相应的图片及视频

>save_mongo()：存入mongodb中


## 截图功能

获取已经存入mongodb中的每个帖子的url，screenshot.py实现了对每篇帖子截图的功能。

截图功能的运行顺序：

1、master.py：从数据库中加载url至redis队列中备用

2、screenshot.py：截图程序

>get_url()：
  
>>从redis队列中获取到待爬取的帖子url；
    
>>根据url从mongodb中获取帖子信息；
    
>>根据帖子信息中的时间戳，创建相应的文件路径；
    
>>加载webdriver用于帖子爬取

>get_picture()：

>>利用selenium+phantomjs打开帖子的url；

>>利用webdriver的截图功能实现截图


# 数据存储结构

在MongoDB中，每个帖子以一条信息的方式存储，每条信息的具体字段意义如下表所示：

key | 意义
-------- | --------
_id	| 帖子的时间戳
taken_at_timestamp	| 帖子的时间戳
url	| 帖子的地址(https://www.instagram.com/p/{shortcode}/?taken-by={user})
shortcode | 帖子的标识符，对于每个用户的所有帖子来说是唯一的
typename | 帖子类型
comment_count | 评论数
like_count | 点赞数
text | 帖子内容
media_url | 列表。包含该帖子中的所有图片及视频的url
