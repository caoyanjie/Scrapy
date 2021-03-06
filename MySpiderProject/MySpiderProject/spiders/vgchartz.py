# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
#from scrapy.loader.processors import MapCompose, TakeFirst
from MySpiderProject.items import VgchartzItem


class VgchartzSpider(scrapy.Spider):
    name = 'vgchartz'
    allowed_domains = ['vgchartz.com']
    start_urls = [
        'http://www.vgchartz.com/yearly/2014/Global/',
        #'http://www.vgchartz.com/yearly/2015/Global/',
        #'http://www.vgchartz.com/yearly/2016/Global/',
        #'http://www.vgchartz.com/yearly/2017/Global/',
        #'http://www.vgchartz.com/yearly/2018/Global/',
    ]
    custom_settings = {
    #    'DOWNLOADER_MIDDLEWARES': {'MySpiderProject.middlewares.DelayLoading': 543},
        'ITEM_PIPELINES': {'MySpiderProject.pipelines.VgchartzPipeline': 300}
    }

    def parse(self, response):
        lines = response.xpath('//tr')
        item = VgchartzItem()
        for line in lines:
            data = line.xpath('./td[1]/text()').extract()
            try:
                if not data:
                    continue
                int(data[0])
            except:
                continue

            '''
            item['pos'] = line.xpath('./td[1]/text()').extract_first()
            item['game'] = line.xpath('./td[2]/table/tbody/tr/td[2]/text()').extract_first()
            item['weeks'] = line.xpath('./td[3]/text()').extract_first()
            item['yearly'] = line.xpath('./td[4]/text()').extract_first()
            item['total'] = line.xpath('./td[5]/text()').extract_first()
            yield item
            '''

            item_loader = ItemLoader(item=VgchartzItem(), selector=line)
            item_loader.add_xpath('pos', './td[1]/text()')
            item_loader.add_xpath('game', './td[2]/table/tbody/tr/td[2]/text()')
            item_loader.add_xpath('weeks', './td[3]/text()')
            item_loader.add_xpath('yearly', './td[4]/text()')
            item_loader.add_xpath('total', './td[5]/text()')
            yield item_loader.load_item()

            '''
            # 暂时不知道add_xpath怎么实现extract_firxt()的效果
            item_loader = ItemLoader(item=VgchartzItem(), selector=line)
            item_loader.add_xpath('pos', './td[1]/text()', MapCompose(str.strip), TakeFirst())
            item_loader.add_xpath('game', './td[2]/table/tbody/tr/td[2]/text()', MapCompose(str.strip), TakeFirst())
            item_loader.add_xpath('weeks', './td[3]/text()', MapCompose(str.strip), TakeFirst())
            item_loader.add_xpath('yearly', './td[4]/text()', MapCompose(str.strip), TakeFirst())
            item_loader.add_xpath('total', './td[5]/text()', MapCompose(str.strip), TakeFirst())
            yield item_loader.load_item()
            '''
