网络爬虫-CCNP
此网络爬虫工程以Python语言开发，采用Scrapy框架。 爬取的目标站点是“中国商品网”，抓取供应商下的商品数据。
Documents安装与使用
	1. 安装Python-2.7.x
	2. 安装Scrapy框架
	3. 在工程根路径下执行命令

scrapy crawl CCNP

程序运行结束以后，抓取的商品数据自动存入Mongodb数据库的ccnp集合中。 商品所对应的图片信息保存到当前工程目录下的image路径下。
