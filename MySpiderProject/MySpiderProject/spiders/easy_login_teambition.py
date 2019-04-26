# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class EasyLoginTeambitionSpider(CrawlSpider):
    name = 'easy_login_teambition'
    allowed_domains = ['teambition.com']
    start_urls = ['http://teambition.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@itemprop="url"]'), callback='parse_item'),
    )

    def start_requests(self):
        return [
            Request('https://account.teambition.com/login', callback=self.parse_welcome)
        ]

    def parse_welcome(self, response):
        form_data = {
            'phone': '17521092026',
            'email': '17521092026',
            'password': 'qgdi2018Q',
            #'next_url': response.xpath('//div[@class="tb-auth third-bind-hide"]/a[2]/@href').extract(),
            'token': response.xpath('//script[@id="secrets"]/@data-clienttoken').extract(),
            'client_id': response.xpath('//script[@id="secrets"]/@data-clientid').extract()
        }
        return FormRequest.from_response(response, formdata=form_data)

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
