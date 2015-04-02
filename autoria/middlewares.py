# -*- coding: utf8 -*-

import random

from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware

from autoria.settings import USER_AGENT_LIST


class RandomUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        ua = getattr(spider, 'user_agent', None) or \
             random.choice(USER_AGENT_LIST)

        if ua:
            request.headers.setdefault('User-Agent', ua)
