import os

import errno
from pathlib import Path

from scrapy.spiders.init import Spider
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
import json
import requests
from lxml import html
import re
import logging

logging.basicConfig(filename='crawl.log', filemode="w", level=logging.INFO)

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class MySpider(Spider):
    name = 'esmart'
    root_folder = './data/'
    userid = input('login name: ')
    passwd = input('password: ')
    ebook = input('ebook id: ')

    downloaded = []

    index_page = 'http://www.esmartclass.net/'
    allowed_domains = ['esmartclass.net']
    login_page = 'http://www.esmartclass.net/member/login'
    book_root_path = 'http://www.esmartclass.net/ebook/' + ebook

    if ebook.startswith("SMART_"):
        start_urls = [book_root_path + '/Digitalmain.jsp']
        start_urls.append(book_root_path + '/main.swf')
        start_urls.append(book_root_path + '/contents/intro.swf')
        start_urls.append(book_root_path + '/contents/copyright.swf')

        for n in range(1, 45):
            start_urls.append(book_root_path + '/contents/smart_%d.swf' % n)
        for n in range(1, 11):
            start_urls.append(book_root_path + '/contents/smart_story%d.swf' % n)
        for n in range(1, 11):
            start_urls.append(book_root_path + '/contents/smart_chant%d.swf' % n)
        for n in range(1, 11):
            start_urls.append(book_root_path + '/contents/smart_cartoon%d.swf' % n)
        for n in range(1, 11):
            start_urls.append(book_root_path + '/contents/effects/es%02d.mp3' % n)
            start_urls.append(book_root_path + '/contents/effects/ns%02d.mp3' % n)
            start_urls.append(book_root_path + '/contents/effects/ct%02d.mp3' % n)
        for n in range(1, 11):
            for m in range(1, 3):
                start_urls.append(book_root_path + '/contents/effects/ns%02d-%d.mp3' %(n, m))
        for n in range(1, 16):
            for m in range(1, 16):
                start_urls.append(book_root_path + '/contents/card/card_%d_%d.jpg' % (n, m))
        for n in range(1, 11):
            for m in range(1, 6):
                start_urls.append(book_root_path + '/contents/card/word_%d_%d.jpg' % (n, m))
        for n in range(1, 4):
            for m in range(1, 4):
                start_urls.append(book_root_path + '/contents/NSP%d_%d.swf' % (n, m))

    else:
        start_urls = [book_root_path + '/index.jsp',
                      book_root_path + '/page/contents.jsp']

        start_urls.append(book_root_path + '/game/sound/ending.mp3')
        start_urls.append(book_root_path + '/images/icon/card_sound.png')
        start_urls.append(book_root_path + '/game/sound/ddang.mp3')
        for n in range(1, 60):
            start_urls.append(book_root_path + '/page/page%d.jsp' % n)
            start_urls.append(book_root_path + '/zoom_page/page%d.jsp' % n)
        for n in range(1, 30):
            start_urls.append(book_root_path + '/card/page%d.jsp' % n)
            start_urls.append(book_root_path + '/game/page%d.jsp' % n)
            start_urls.append(book_root_path + '/movie/page%d.html' % n)
            start_urls.append(book_root_path + '/movie/page%d.swf' % n)
        for n in range(1, 110):
            for m in range(1, 5):
                start_urls.append(book_root_path + '/partZoom/page%d_%d.jsp' % (n, m))


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
        logging.info("URL:" + response.url)
        uri = response.url[27:]
        path = self.root_folder + uri.replace(uri.split("/")[-1], "")
        self.makePath(path)

        filename = self.root_folder + uri
        filename = filename.replace(".jsp", ".html")
        with open(filename, 'wb') as f:
            f.write(response.body.replace(b".jsp", b".html"))
        self.downloadSrc(response)


    def downloadSrc(self, response):
        parsed_body = ""
        try:
            parsed_body = html.fromstring(response.text)
        except AttributeError:
            return
        # Grab links to all images
        img = parsed_body.xpath('//./@src')
        css = parsed_body.xpath('//link/@href')
        mp3 = re.findall(r"aud_play_pause[\d]?\('(.*)mp3'", response.text)
        card = []
        try:
            card = re.findall(r"Array\((\".*\")\);", response.text)[0].replace("\"", "").split(",")
        except IndexError:
            pass

        # Convert any relative urls to absolute urls
        images = [self.book_root_path + '/images/icon/play.png', self.book_root_path + '/images/icon/pause.png',
                  self.book_root_path + '/images/icon/pause_s.png']
        images = images + [urljoin(response.url, url) for url in img]
        images = images + [urljoin(response.url, url) for url in css]
        images = images + [urljoin(response.url, url + 'mp3') for url in mp3]
        images = images + [urljoin(response.url, '../images/flashcard/' + url + '.jpg') for url in card]
        images = images + [urljoin(response.url, '../images/flashcard/' + url + '_word.jpg') for url in card]
        images = images + [urljoin(response.url, '../audio/flashcard/F_' + url + '.mp3') for url in card]
        images = images + [urljoin(response.url, '../images/game/' + url + '.png') for url in card]
        images = images + [urljoin(response.url, '../images/game/' + url + '_word.png') for url in card]

        logging.info(images)

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
        file = self.root_folder + uri
        f = open(file, 'wb')  ## add the folder name
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
