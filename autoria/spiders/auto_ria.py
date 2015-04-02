# -*- coding: utf-8 -*-

import json
import random
import urlparse

import scrapy

from scrapy.contrib.loader.processor import TakeFirst

from scrapy.http import Request

from scrapy.selector import Selector

from scrapy.utils.response import get_base_url

from autoria.loaders import AutoItemLoader
from autoria.spiders import AJAX_HEADERS


class AutoRiaSpider(scrapy.Spider):
    name = 'auto.ria.com'
    allowed_domains = ['auto.ria.com']
    # allowed_models = ['kia', 'ford', 'renault', 'hyundai', 'skoda', 'seat', 'peugeot', 'dacia', 'volkswagen', 'mitsubishi']
    exclude_models = [u'газ', u'ваз', u'заз', u'daewoo', u'samand',
                      u'chevrolet', u'byd', u'geely', u'great wall', u'богдан',
                      u'chery']
    start_urls = ("http://auto.ria.com/",)

    CAR_URL = 'http://auto.ria.com/blocks_search/view/auto/{}/?lang_id=2&view_type_id=0&price_for_hot=40&price_for_fishka=1&strategy=default&domain_zone=com&user_id=0'
    PARSE_URL = "http://auto.ria.com/blocks_search_ajax/search/?countpage=10&category_id=1&view_type_id=0&page={page}&marka=0&model=0&s_yers=2005&po_yers=0&state=7&city=7&price_ot=5000&price_do=9001&currency=1&gearbox=1&type=0&drive_type=0&door=0&color=0&metallic=0&engineVolumeFrom=&engineVolumeTo=&raceFrom=5&raceTo=70&powerFrom=&powerTo=&power_name=1&fuelRateFrom=&fuelRateTo=&fuelRatesType=city&custom=1&damage=1&saledParam=2&under_credit=0&confiscated_car=0&auto_repairs=2&with_exchange=0&with_real_exchange=0&exchangeTypeId=0&with_photo=1&with_video=0&is_hot=0&vip=0&checked_auto_ria=0&top=0&order_by=0&hide_black_list=0&auto_id=&deletedAutoSearch=0&user_id=0&scroll_to_auto_id=0&expand_search=0&can_be_checked=0&last_auto_id=0&matched_country=-1&seatsFrom=&seatsTo=&wheelFormulaId=0&axleId=0&carryingTo=&carryingFrom=&search_near_states=0&company_id=0&company_type=0&__={rnd}"
    REFERER_URL = "http://auto.ria.com/search/?countpage=10&category_id=1&view_type_id=0&page={page}&marka=0&model=0&s_yers=2005&po_yers=0&state=7&city=7&price_ot=5000&price_do=9001&currency=1&gearbox=1&type=0&drive_type=0&door=0&color=0&metallic=0&engineVolumeFrom=&engineVolumeTo=&raceFrom=5&raceTo=70&powerFrom=&powerTo=&power_name=1&fuelRateFrom=&fuelRateTo=&fuelRatesType=city&custom=1&damage=1&saledParam=2&under_credit=0&confiscated_car=0&auto_repairs=2&with_exchange=0&with_real_exchange=0&exchangeTypeId=0&with_photo=1&with_video=0&is_hot=0&vip=0&checked_auto_ria=0&top=0&order_by=0&hide_black_list=0&auto_id=&deletedAutoSearch=0&user_id=0&scroll_to_auto_id=0&expand_search=0&can_be_checked=0&last_auto_id=0&matched_country=-1&seatsFrom=&seatsTo=&wheelFormulaId=0&axleId=0&carryingTo=&carryingFrom=&search_near_states=0&company_id=0&company_type=0"

    def parse(self, response):
        yield Request(
            url=self.PARSE_URL.format(page=0, rnd=random.randint(0, 2000000)),
            headers=AJAX_HEADERS,
            callback=self.search_items)

    def search_items(self, response):
        data = json.loads(response.body_as_unicode())
        ids = data.get('result', {}).get('search_result', {}).get('ids', [])
        page_num = int(data.get('additional_params', {}).get('page', '0'))

        if not ids:
            return

        headers = AJAX_HEADERS.copy()
        headers['Referer'] = self.REFERER_URL.format(page=0)

        yield Request(url=self.PARSE_URL.format(page=page_num + 1,
                                                rnd=random.randint(0,
                                                                   2000000)),
                      headers=headers, callback=self.search_items)

        for uid in ids:
            yield Request(url=self.CAR_URL.format(uid), headers=headers,
                          meta={'uid': uid},
                          callback=self.parse_item)

    def parse_item(self, response):
        base_url = get_base_url(response)
        selector = Selector(response)
        # selector = Selector(text=response.body.decode('utf-8'))
        loader = AutoItemLoader(selector=selector)

        uid = response.meta['uid']
        item_url = urlparse.urljoin(base_url, TakeFirst()(
            selector.xpath('//a[@nav_mem="{}"]/@href'.format(uid)).extract()))

        title = TakeFirst()(selector.xpath(
            '//a[@nav_mem="{}"]/@title'.format(uid)).extract()).lower()
        if any(model in title for model in self.exclude_models):
            self.log(u'Excluded: {}'.format(title))
            return

        loader.add_value('uid', uid)
        loader.add_value('link', item_url)
        loader.add_value('title', title)
        loader.add_xpath('desc', '//p[@class="descriptions-ticket"]/text()')
        loader.add_xpath('prise_hrn',
                         '//div[@class="price"]//*[@title="UAH"]/text()',
                         re=u'(.+) грн.')
        loader.add_xpath('prise_usd',
                         '//div[@class="price"]//*[@title="USD"]/text()')
        loader.add_xpath('is_auction',
                         '//i[@class="icon-auction"]')
        loader.add_xpath('year', '//h3[@class="head-car"]/a/@title',
                         re='.+(\d{4})$')
        loader.add_xpath('mileage',
                         '//i[@class="icon-char-mileage"]/../text()')
        loader.add_xpath('fuel', '//i[@class="icon-char-fuel"]/../text()')
        loader.add_xpath('created_at', '//span[@class="date-add"]/@pvalue')
        # loader.add_xpath('author', '//span[@class="date-add"]/@pvalue')
        loader.add_xpath('author_phone',
                         '//div[@class="contact-seller"]/span[@class="phone"]/text()')
        # loader.add_xpath('author_ads_count', '//div[@class="contact-seller"]/span[@class="phone"]/text()')

        yield loader.load_item()
