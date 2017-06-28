import os

import errno
from scrapy.spiders.init import Spider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from selenium import webdriver
from scrapy.exceptions import CloseSpider
import json
import requests
from lxml import html
import re
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class MySpider(Spider):
    name = 'esmart'
    root_folder = './data/'
    userid = raw_input('login name: ')
    passwd = raw_input('password: ')
    ebook = raw_input('ebook id: ')

    downloaded = []

    index_page = 'http://www.esmartclass.net/'
    allowed_domains = ['esmartclass.net']
    login_page = 'http://www.esmartclass.net/member/login'
    book_root_path = 'http://www.esmartclass.net/ebook/' + ebook
    start_urls = [ book_root_path + '/index.jsp',
                   book_root_path + '/page/contents.jsp',
                   book_root_path + '/page/page1.jsp',
                   book_root_path + '/page/page2.jsp',
                   book_root_path + '/page/page3.jsp',
                   book_root_path + '/page/page4.jsp',
                   book_root_path + '/page/page5.jsp',
                   book_root_path + '/page/page6.jsp',
                   book_root_path + '/page/page7.jsp',
                   book_root_path + '/page/page8.jsp',
                   book_root_path + '/page/page9.jsp',
                   book_root_path + '/page/page10.jsp',
                   book_root_path + '/page/page11.jsp',
                   book_root_path + '/page/page12.jsp',
                   book_root_path + '/page/page13.jsp',
                   book_root_path + '/page/page14.jsp',
                   book_root_path + '/page/page15.jsp',
                   book_root_path + '/page/page16.jsp',
                   book_root_path + '/page/page17.jsp',
                   book_root_path + '/page/page18.jsp',
                   book_root_path + '/page/page19.jsp',
                   book_root_path + '/page/page20.jsp',
                   book_root_path + '/page/page21.jsp',
                   book_root_path + '/page/page22.jsp',
                   book_root_path + '/page/page23.jsp',
                   book_root_path + '/page/page24.jsp',
                   book_root_path + '/page/page25.jsp',
                   book_root_path + '/page/page26.jsp',
                   book_root_path + '/page/page27.jsp',
                   book_root_path + '/page/page28.jsp',
                   book_root_path + '/page/page29.jsp',
                   book_root_path + '/page/page30.jsp',
                   book_root_path + '/zoom_page/page1.jsp',
                   book_root_path + '/zoom_page/page2.jsp',
                   book_root_path + '/zoom_page/page3.jsp',
                   book_root_path + '/zoom_page/page4.jsp',
                   book_root_path + '/zoom_page/page5.jsp',
                   book_root_path + '/zoom_page/page6.jsp',
                   book_root_path + '/zoom_page/page7.jsp',
                   book_root_path + '/zoom_page/page8.jsp',
                   book_root_path + '/zoom_page/page9.jsp',
                   book_root_path + '/zoom_page/page10.jsp',
                   book_root_path + '/zoom_page/page11.jsp',
                   book_root_path + '/zoom_page/page12.jsp',
                   book_root_path + '/zoom_page/page13.jsp',
                   book_root_path + '/zoom_page/page14.jsp',
                   book_root_path + '/zoom_page/page15.jsp',
                   book_root_path + '/zoom_page/page16.jsp',
                   book_root_path + '/zoom_page/page17.jsp',
                   book_root_path + '/zoom_page/page18.jsp',
                   book_root_path + '/zoom_page/page19.jsp',
                   book_root_path + '/zoom_page/page20.jsp',
                   book_root_path + '/zoom_page/page21.jsp',
                   book_root_path + '/zoom_page/page22.jsp',
                   book_root_path + '/zoom_page/page23.jsp',
                   book_root_path + '/zoom_page/page24.jsp',
                   book_root_path + '/zoom_page/page25.jsp',
                   book_root_path + '/zoom_page/page26.jsp',
                   book_root_path + '/zoom_page/page27.jsp',
                   book_root_path + '/zoom_page/page28.jsp',
                   book_root_path + '/zoom_page/page29.jsp',
                   book_root_path + '/zoom_page/page30.jsp',
                  ]

    def __init__(self):
        self.driver = webdriver.PhantomJS

    def start_requests(self):
        yield Request(
            url=self.index_page,
            callback=self.login,
            dont_filter=True
        )

    def login(self, response):
        """Generate a login request."""
        return Request(url=self.login_page, method='POST',
                       body=json.dumps({'userid': self.userid, 'passwd': self.passwd}),
                       headers={'Content-Type': 'application/json'},
                       callback=self.check_login_response)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if bytearray(self.userid, 'utf-8') not in response.body:
            # if self.userid not in response.body:
            self.log("Bad times :(")
            raise CloseSpider('Login failed')
            return
            # Something went wrong, we couldn't log in, so nothing happens.

        for url in self.start_urls:
            # yield self.make_requests_from_url(url)
            yield Request(url, dont_filter=True)  # callback=self.parse

    def parse(self, response):
        uri = response.url[27:]
        path = self.root_folder + uri.replace(uri.split("/")[-1], "")
        self.makePath(path)

        filename = self.root_folder + uri.split(".")[0] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body.replace(b".jsp", b".html"))
        self.downloadSrc(response)

    def downloadSrc(self, response):

        parsed_body = html.fromstring(response.text)
        # Grab links to all images
        img = parsed_body.xpath('//./@src')
        css = parsed_body.xpath('//link/@href')
        mp3 = re.findall(r"aud_play_pause[\d]?\('(.*)mp3'", response.text)

        # Convert any relative urls to absolute urls
        images = [self.book_root_path + '/images/icon/play.png', self.book_root_path + '/images/icon/pause.png', self.book_root_path + '/images/icon/pause_s.png' ]
        images = images + [urljoin(response.url, url) for url in img]
        images = images + [urljoin(response.url, url) for url in css]
        images = images + [urljoin(response.url, url + 'mp3') for url in mp3]

        # Only download first x 10
        for contentUrl in images[0:1000]:  ## 100 will scrape 100 pictures
            if contentUrl in self.downloaded:
                continue
            ext = contentUrl.split(".")[-1]
            if "jsp" in ext:
                continue
            r = self.downloadContent(contentUrl)
            self.downloaded = self.downloaded + [contentUrl]

            if "css" in ext:
                cssimg = [urljoin(contentUrl, url) for url in re.findall(r"url\((.*)\) ", r.content.decode('utf-8'))]
                for imgUrl in cssimg[0:1000]:  ## 100 will scrape 100 pictures
                    self.downloadContent(imgUrl)

    def downloadContent(self, url):
        uri = url[27:]
        path = self.root_folder + uri.replace(uri.split("/")[-1], "")
        self.makePath(path)
        img = requests.get(url)
        f = open(self.root_folder + uri, 'wb')  ## add the folder name
        f.write(img.content)
        f.close()
        return img

    def makePath(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise
