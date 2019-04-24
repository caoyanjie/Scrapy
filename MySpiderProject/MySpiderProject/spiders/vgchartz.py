# -*- coding: utf-8 -*-
import scrapy
from MySpiderProject.items import MyspiderprojectItem


class VgchartzSpider(scrapy.Spider):
    name = 'vgchartz'
    allowed_domains = ['vgchartz.com']
    start_urls = [
    	'http://www.vgchartz.com/yearly/2014/Global/',
    	'http://www.vgchartz.com/yearly/2015/Global/',
    	'http://www.vgchartz.com/yearly/2016/Global/',
    	'http://www.vgchartz.com/yearly/2017/Global/',
    	'http://www.vgchartz.com/yearly/2018/Global/',
    ]

    def parse(self, response):
        lines = response.xpath('//tr')
        item = MyspiderprojectItem()
        for line in lines:
            data = line.xpath('./td[1]/text()').extract()
            try:
                if not data:
                    continue
                int(data[0])
            except:
                continue
            item['Pos'] = data = line.xpath('./td[1]/text()').extract()
            item['Game'] = line.xpath('./td[2]/table/tbody/tr/td[2]/text()').extract()
            item['Weeks'] = line.xpath('./td[3]/text()').extract()
            item['Yearly'] = line.xpath('./td[4]/text()').extract()
            item['Total'] = line.xpath('./td[5]/text()').extract()
            yield item

