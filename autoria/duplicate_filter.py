# -*- coding: utf-8 -*-

from scrapy.dupefilter import RFPDupeFilter


class SeenURLFilter(RFPDupeFilter):
    """A dupe filter that considers the URL"""

    def __init__(self, path=None, debug=False):
        self.urls_seen = set()
        super(SeenURLFilter, self).__init__(path, debug)

    def request_seen(self, request):
        if request.url in self.urls_seen:
            return True
        else:
            self.urls_seen.add(request.url)