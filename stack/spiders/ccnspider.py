#!/usr/bin/env python
# -*- coding:utf-8 -*-
from urllib import unquote

import scrapy
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from stack.items import CcnItem

global page_type
class CcnSpider(BaseSpider):
    name = 'CCN'

    download_delay = 1
    allowed_domains = ["ccn.mofcom.gov.cn"]
    start_urls = [
        # 包装机械
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=9&keyword=%B0%FC%D7%B0%BB%FA%D0%B5&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=10&keyword=%B0%FC%D7%B0%BB%FA%D0%B5&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=11&keyword=%B0%FC%D7%B0%BB%FA%D0%B5&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=12&keyword=%B0%FC%D7%B0%BB%FA%D0%B5&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=13&keyword=%B0%FC%D7%B0%BB%FA%D0%B5&queryType=company&description=&firstHscode=&firstPname=",
        # 泵
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=14&keyword=%B1%C3&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=15&keyword=%B1%C3&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=16&keyword=%B1%C3&queryType=company&description=&firstHscode=&firstPname=",
        # 食品机械
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=8&keyword=%CA%B3%C6%B7%BB%FA%D0%B5&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=9&keyword=%CA%B3%C6%B7%BB%FA%D0%B5&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=10&keyword=%CA%B3%C6%B7%BB%FA%D0%B5&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=11&keyword=%CA%B3%C6%B7%BB%FA%D0%B5&queryType=company&description=&firstHscode=&firstPname=",
        # 船舶
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=3&keyword=%B4%AC%B2%B0&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=4&keyword=%B4%AC%B2%B0&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=5&keyword=%B4%AC%B2%B0&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=6&keyword=%B4%AC%B2%B0&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=7&keyword=%B4%AC%B2%B0&queryType=company&description=&firstHscode=&firstPname=",
        # 衡器
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=5&keyword=%BA%E2%C6%F7&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=6&keyword=%BA%E2%C6%F7&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=7&keyword=%BA%E2%C6%F7&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=8&keyword=%BA%E2%C6%F7&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=9&keyword=%BA%E2%C6%F7&queryType=company&description=&firstHscode=&firstPname=",
        # 链条
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=4&keyword=%C1%B4%CC%F5&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=8&keyword=%C1%B4%CC%F5&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=9&keyword=%C1%B4%CC%F5&queryType=company&description=&firstHscode=&firstPname=",
        # 家用电器
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=2&keyword=%BC%D2%D3%C3%B5%E7%C6%F7&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=3&keyword=%BC%D2%D3%C3%B5%E7%C6%F7&queryType=company&description=&firstHscode=&firstPname=",
        # 仪器仪表
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=13&keyword=%D2%C7%C6%F7%D2%C7%B1%ED&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=14&keyword=%D2%C7%C6%F7%D2%C7%B1%ED&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=15&keyword=%D2%C7%C6%F7%D2%C7%B1%ED&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=16&keyword=%D2%C7%C6%F7%D2%C7%B1%ED&queryType=company&description=&firstHscode=&firstPname=",
        # 运输设备
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=10&keyword=%B3%B5&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=11&keyword=%B3%B5&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=12&keyword=%B3%B5&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=13&keyword=%B3%B5&queryType=company&description=&firstHscode=&firstPname=",
        "http://ccn.mofcom.gov.cn/myccn/QueryAction.do?currentPage=14&keyword=%B3%B5&queryType=company&description=&firstHscode=&firstPname="
    ]

    def parse(self, response):
        global page_type
        sel = Selector(response)
        ###items = []
        str_star =  response.url.find('%')
        str_end = response.url.find('&queryType')
        page_type =  unquote(response.url[str_star:str_end]).decode('gbk')
        companys = sel.xpath('//a[@valign="bottom"]')

        n = 0
        for company in companys:
            item = CcnItem()
            n = n + 1 
            ###print n
            ###print '>>> company = ' + company.extract() 
            title = company.xpath('text()').extract()            
            link = company.xpath('@href').extract()

            for item_url in link:
                item_url = 'http://ccn.mofcom.gov.cn' + item_url
                print '>>> item_url =' + item_url
                request = scrapy.Request(item_url,
                                         callback=self.parse_item)
                request.meta['page_type'] = page_type
                yield request
                #yield Request(url=item_url ,callback=self.parse_item)
        '''        
            item['cname'] = [t.encode('utf-8') for t in title]
            item['curl'] = ['http://ccn.mofcom.gov.cn' + l.encode('utf-8') for l in link]
            items.append(item)

        return items
        '''

    def parse_item(self, response):
        print '>>> url=' +  response.url
        if response.status == 200:
            sel = Selector(response)
            cinfo = sel.xpath('//div[@class="qy_r_box1"]')

            for info in cinfo:
                item = CcnItem()
                item['proType'] = response.meta['page_type']
                keys = info.xpath('.//table//tr//td//i//text()').extract()
                data  = info.xpath('.//table/tr/td')
                values = data.xpath('string(.)').extract()
                conInfo = info.xpath('//div[@class]//p/text()').extract()
                for i in conInfo:
                    if u'销售负责人' in i:
                        item['contUserNameCN'] = i.split(u'：')[1]
                    if u'联系电话' in i:
                        item['comTelephone'] = i.split(u'：')[1]
                    if u'移动电话' in i:
                        item['comTelephone'] = item['comTelephone'] + i.split(u'：')[1]
                        break
                for key in keys: 
                    for value in values:
                        if key in value:
                            print '>>> value = ' + value
                            s = value.split(u'：')
                            ###print s[0] + ':' + s[1]
                            if u'企业名称' in key:
                                item['comNameCn'] = s[1]
                            if u'通讯地址' in key:
                                item['comAddressCn'] = s[1]   
                            if u'经营范围' in key:
                                item['comScpoe'] = s[1]
                            if u'经营性质' in key:
                                item['comTypeCn'] = s[1]
                            if u'成立年份' in key:
                                item['timeEstablished'] = s[1][0:4]
                            if u'雇员人数' in key:
                                item['staffFactory'] = s[1]
                                print '>>> staffFactory = '+  item['staffFactory']
                            if u'注册资本' in key:
                                item['comRegCapital'] = s[1]
                            if u'法人代表' in key:
                                item['legalUserNameCn'] = s[1]
                                print '>>> legalUserNameCn = ' + item['legalUserNameCn']
                if len(item) != 0:
                    item['url']=response.url
                    yield item
                '''
                for value in values:
                    print '>>> 1 value = ' + value
                    if '' == value or  ' ' == value:
                        continue
                    print '>>> 2 value = ' + value
                    if any(value):
                        print '>>>> any() is True'
                        s = value.split(u'：')
                        if '' == s[1]:
                            print '>>>>>>>>>> s[1] = ' + s[1]
                            continue
                        print '>>> s = ' +  s[0] + ':' + s[1]
                        if u'企业名称' in s[0]:
                            item['comNameCn'] = s[1]
                        if u'通讯地址' in s[0]:
                            item['comAddressCn'] = s[1]   
                        if u'经营范围' in s[0]:
                            item['comScpoe'] = s[1]
                        if u'经营性质' in s[0]:
                            item['comTypeCn'] = s[1]
                        if u'成立年份' in s[0]:
                            item['timeEstablished'] = s[1][0:4]
                        if u'雇员人数' in s[0]:
                            item['staffFactory'] = s[1]
                        if u'注册资本' in s[0]:
                            item['comRegCapital'] = s[1]
                        if u'法人代表' in s[0]:
                            item['legalUserNameCn'] = s[1]
                if len(item) != 0:
                    yield item
                '''
        ###return items




