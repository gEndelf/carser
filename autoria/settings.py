# -*- coding: utf-8 -*-

BOT_NAME = 'autoria'

SPIDER_MODULES = ['autoria.spiders']
NEWSPIDER_MODULE = 'autoria.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'

DUPEFILTER_CLASS = 'autoria.duplicate_filter.SeenURLFilter'
DOWNLOAD_DELAY = 3
REFERER_ENABLED = False
COOKIES_ENABLED = True

HTTPCACHE_ENABLED = False

HEADERS = {
    'Accept-Language': 'en-US,en;q=0.8,ja;q=0.6,vi;q=0.4',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    }

try:
    from autoria.local_settings import *
except ImportError:
    pass

