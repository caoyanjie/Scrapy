# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class MyspiderprojectItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    address = scrapy.Field()
    image_url = scrapy.Field()
    

class AreaItem(scrapy.Item):
    data = scrapy.Field()
    city = scrapy.Field()
    aqi = scrapy.Field()    #空气质量指数
    level = scrapy.Field()  #空气质量等级
    pm2_5 = scrapy.Field()  #pm2.5
    pm10 = scrapy.Field()
    so2 = scrapy.Field()
    co = scrapy.Field()
    no2 = scrapy.Field()
    o3 = scrapy.Field()


class StockItem(scrapy.Item):
    昨收 = scrapy.Field()
    当日幅度 = scrapy.Field()
    收益 = scrapy.Field()
    开盘 = scrapy.Field()
    周范围 = scrapy.Field()
    每股收益 = scrapy.Field()
    量 = scrapy.Field()
    市值 = scrapy.Field()
    红利 = scrapy.Field()
    平均成交量 = scrapy.Field()
    市盈率 = scrapy.Field()
    贝塔 = scrapy.Field()
    一年涨跌幅 = scrapy.Field()
    发行股份 = scrapy.Field()
    下一个盈利日 = scrapy.Field()


class VgchartzItem(scrapy.Item):
    #default_input_processor = TakeFirst()
    #default_output_processor = TakeFirst()

    '''
    pos = scrapy.Field()
    game = scrapy.Field()
    weeks = scrapy.Field()
    yearly = scrapy.Field()
    total = scrapy.Field()
    '''

    pos = scrapy.Field(output_processor=TakeFirst())
    game = scrapy.Field(output_processor=TakeFirst())
    weeks = scrapy.Field(output_processor=TakeFirst())
    yearly = scrapy.Field(output_processor=TakeFirst())
    total = scrapy.Field(output_processor=TakeFirst())
