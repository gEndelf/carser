# -*- coding: utf-8 -*-

import scrapy


class AutoItem(scrapy.Item):
    uid = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    prise_hrn = scrapy.Field()
    prise_usd = scrapy.Field()
    is_auction = scrapy.Field()
    year = scrapy.Field()
    mileage = scrapy.Field()
    fuel = scrapy.Field()
    created_at = scrapy.Field()
    author = scrapy.Field()
    author_phone = scrapy.Field()
    author_ads_count = scrapy.Field()