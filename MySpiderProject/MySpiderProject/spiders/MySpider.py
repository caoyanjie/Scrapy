# -*- coding: utf-8 -*-
import scrapy

from MySpiderProject.items import MyspiderprojectItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from urllib.parse import urlparse, urljoin


class MyspiderSpider(scrapy.Spider):
    name = 'MySpider'
    allowed_domains = ['scrapybook.s3.amazonaws.com']

    start_urls = [
        'http://scrapybook.s3.amazonaws.com/properties/property_000000.html',
        'http://scrapybook.s3.amazonaws.com/properties/property_000001.html',
        'http://scrapybook.s3.amazonaws.com/properties/property_000002.html',
    ]

    def parse(self, response):
        """
        print(f'''title: {response.xpath('//*[@itemprop="name"][1]/text()').extract()}''')
        print(f'''price: {response.xpath('//*[@itemprop="price"][1]/text()').extract()}''')
        print(f'''description: {response.xpath('//*[@itemprop="description"][1]/text()').extract()}''')
        print(f'''address: {response.xpath('//*[@itemtype="htpp://schema.org/Place"][1]/text()').extract()}''')
        print(f'''image_url: {response.xpath('//*[@itemprop="image"][1]/@src').extract()}''')
        """

        '''
        item = MyspiderprojectItem()
        item['title'] = response.xpath('//*[@itemprop="name"][1]/text()').extract()
        item['price'] = response.xpath('//*[@itemprop="price"][1]/text()').extract()
        item['description'] = response.xpath('//*[@itemprop="description"][1]/text()').extract()
        item['address'] = response.xpath('//*[@itemtype="htpp://schema.org/Place"][1]/text()').extract()
        item['image_url'] = response.xpath('//*[@itemprop="image"][1]/@src').extract()
        return item
        '''

        '''
        item_loader = ItemLoader(item=MyspiderprojectItem(), response=response)
        item_loader.add_xpath('title', '//*[@itemprop="name"][1]/text()')
        item_loader.add_xpath('price', '//*[@itemprop="price"][1]/text()')
        item_loader.add_xpath('description', '//*[@itemprop="description"][1]/text()')
        item_loader.add_xpath('address', '//*[@itemtype="htpp://schema.org/Place"][1]/text()')
        item_loader.add_xpath('image_url', '//*[@itemprop="image"][1]/@src')
        return item_loader.load_item()
        '''

        item_loader = ItemLoader(item=MyspiderprojectItem(), response=response)
        item_loader.add_xpath('title', '//*[@itemprop="name"][1]/text()', MapCompose(str.strip, str.title))
        item_loader.add_xpath('price', '//*[@itemprop="price"][1]/text()', MapCompose(lambda i : i.replace(',', ''), float), re='[,.0-9]+')
        item_loader.add_xpath('description', '//*[@itemprop="description"][1]/text()', MapCompose(str.strip), Join())
        item_loader.add_xpath('address', '//*[@itemtype="htpp://schema.org/Place"][1]/text()', MapCompose(str.strip))
        item_loader.add_xpath('image_url', '//*[@itemprop="image"][1]/@src', MapCompose(lambda i : urljoin(response.url, i)))
        return item_loader.load_item()
