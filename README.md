# Car parsers - carser

## Auto-RIA parser

http://auto.ria.com/

Usage:
------

```scrapy crawl auto.ria.com -o cars.csv -a city=[city id] -a state=[state id]```

* **city id** - city ID from auto.ria.ua
* **state id** - region ID from auto.ria.ua

Configuration:
--------------

* **AutoRiaSpider.PARSE_URL** - change search criteria
* **AutoRiaSpider.allowed_models** - (if defined) searching ONLY by this models 
* **AutoRiaSpider.exclude_models** - (if defined) exclude this models
* Results will be saved to **cars.csv**
* more details by app structure & customization: http://scrapy.org
