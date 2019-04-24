# -*- coding: utf-8 -*-
import scrapy

from MySpiderProject.items import MyspiderprojectItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from urllib.parse import urlparse, urljoin

from scrapy.http import Request


class TwoDimensionnalSpider(scrapy.Spider):
    name = 'two_dimensionnal'
    allowed_domains = ['scrapybook.s3.amazonaws.com']
    start_urls = [
        'http://scrapybook.s3.amazonaws.com/properties/index_00000.html',
    ]

    def parse(self, response):
        next_selector = response.xpath('//*[contains(@class, "next")]//@href')
        for url in next_selector.extract():
            yield Request(urljoin(response.url, url))

        item_selector = response.xpath('//*[@itemprop="url"]/@href')
        for url in item_selector.extract():
            yield Request(urljoin(response.url, url), callback=self.parse_item)

    def parse_item(self, response):
        item_loader = ItemLoader(item=MyspiderprojectItem(), response=response)
        item_loader.add_xpath('title', '//*[@itemprop="name"][1]/text()', MapCompose(str.strip, str.title))
        item_loader.add_xpath('price', '//*[@itemprop="price"][1]/text()', MapCompose(lambda i : i.replace(',', ''), float), re='[,.0-9]+')
        item_loader.add_xpath('description', '//*[@itemprop="description"][1]/text()', MapCompose(str.strip), Join())
        item_loader.add_xpath('address', '//*[@itemtype="htpp://schema.org/Place"][1]/text()', MapCompose(str.strip))
        item_loader.add_xpath('image_url', '//*[@itemprop="image"][1]/@src', MapCompose(lambda i : urljoin(response.url, i)))
        return item_loader.load_item()