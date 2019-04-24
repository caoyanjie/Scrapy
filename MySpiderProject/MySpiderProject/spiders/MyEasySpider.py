# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from MySpiderProject.items import MyspiderprojectItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from urllib.parse import urlparse, urljoin


class MyeasyspiderSpider(CrawlSpider):
    name = 'MyEasySpider'
    allowed_domains = ['scrapybook.s3.amazonaws.com']
    start_urls = ['http://scrapybook.s3.amazonaws.com/properties/index_00000.html']

    rules = (
        #Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[contains(@class, "next")]')),
        Rule(LinkExtractor(restrict_xpaths='//*[@itemprop="url"]'), callback='parse_item'),
    )

    def parse_item(self, response):
        #item = {}
        ##item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        ##item['name'] = response.xpath('//div[@id="name"]').get()
        ##item['description'] = response.xpath('//div[@id="description"]').get()
        #return item
        item_loader = ItemLoader(item=MyspiderprojectItem(), response=response)
        item_loader.add_xpath('title', '//*[@itemprop="name"][1]/text()', MapCompose(str.strip, str.title))
        item_loader.add_xpath('price', '//*[@itemprop="price"][1]/text()', MapCompose(lambda i : i.replace(',', ''), float), re='[,.0-9]+')
        item_loader.add_xpath('description', '//*[@itemprop="description"][1]/text()', MapCompose(str.strip), Join())
        item_loader.add_xpath('address', '//*[@itemtype="htpp://schema.org/Place"][1]/text()', MapCompose(str.strip))
        item_loader.add_xpath('image_url', '//*[@itemprop="image"][1]/@src', MapCompose(lambda i : urljoin(response.url, i)))
        return item_loader.load_item()
