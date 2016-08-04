网络爬虫-CCNP
===================


此网络爬虫工程以Python语言开发，采用Scrapy框架。
爬取的目标站点是“中国商品网”，抓取供应商下的商品数据。

----------


Documents
-------------


### 安装与使用

1. 安装Python-2.7.x
2. 安装Scrapy框架
3. 在工程根路径下执行命令

```
scrapy crawl CCNP
```
在settings.py中对mongdb的相关配置进行设置
数据会直接导入mongdb中