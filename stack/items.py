# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class StackItem(Item):
    title = Field()
    url = Field()

class ProductItem(Item):
    company = Field()
    name = Field()
    picture = Field()
    model = Field()
    description = Field()

class CcnItem(Item):
    supplier= Field()
    contUserNameCN = Field()
    legalUserNameCn = Field()
    comTelephone = Field()
    comAddressCn = Field()
    comNameCn = Field()
    comTypeCn = Field()
    comScpoe = Field()
    timeEstablished = Field()
    staffFactory = Field()
    comRegCapital = Field()
    url = Field()
    proType = Field()