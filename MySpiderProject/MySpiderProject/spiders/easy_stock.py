# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from MySpiderProject.items import StockItem
from scrapy.loader import ItemLoader


class EasyStockSpider(CrawlSpider):
    name = 'easy_stock'
    allowed_domains = ['cn.investing.com']
    start_urls = ['https://cn.investing.com/equities/vietnam']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//td[2]'), callback='parse_item'),
    )

    def parse_item(self, response):
        item_loader = ItemLoader(item=StockItem(), response=response)
        item_loader.add_xpath('昨收', '//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[1]/span[2]/text()')
        item_loader.add_xpath('当日幅度', '//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[2]/span[2]/text()')
        item_loader.add_xpath('收益', '//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[3]/span[2]/text()')
        item_loader.add_xpath('开盘', '//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[4]/span[2]/text()')
        item_loader.add_xpath('周范围', '//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[5]/span[2]/text()')
        item_loader.add_xpath('每股收益', '//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[6]/span[2]/text()')
        item_loader.add_xpath('量', '//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[1]/span[7]/text()')
        item_loader.add_xpath('市值', '//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[5]/span[8]/text()')
        item_loader.add_xpath('红利', '//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[1]/span[9]/text()')
        item_loader.add_xpath('平均成交量', '//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[10]/span[2]/text()')
        item_loader.add_xpath('市盈率', '//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[11]/span[2]/text()')
        item_loader.add_xpath('贝塔', '//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[12]/span[2]/text()')
        item_loader.add_xpath('一年涨跌幅', '//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[13]/span[2]/text()')
        item_loader.add_xpath('发行股份', '//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[8]/span[14]/text()')
        item_loader.add_xpath('下一个盈利日', '//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[1]/span[15]/text()')
        return item_loader.load_item()
