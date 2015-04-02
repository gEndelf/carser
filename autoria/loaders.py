# -*- coding: utf-8 -*-

from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, Compose, Join

from autoria.items import AutoItem


class AutoItemLoader(ItemLoader):
    default_item_class = AutoItem
    default_output_processor = Compose(TakeFirst(), lambda x: x.strip())
    is_auction_out = Compose(TakeFirst(), lambda x: True if x else False)
    mileage_out = Compose(Join(), lambda x: x.strip())
    fuel_out = Compose(Join(), lambda x: x.strip())
