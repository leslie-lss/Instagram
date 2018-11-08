# Instagram
爬取Instagram上某一账户的全部post，包括正文，点赞数，评论数，发帖时间，帖子链接，并且下载相应的图片或视频

## need set
需要填写user的名字

利用getCookie.py获取cookie备用

在instagram的用户主页按下F12，获取对应的query_hash以及cookie中的sessionid

此爬虫还将数据信息存储进入mongodb中，可以选择

## 截图功能

获取已经存入mongodb中的每个帖子的url，screenshot.py实现了对每篇帖子截图的功能。
