# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

#\!===========
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time


class AreaSpiderMiddleware(object):
    def __init__(self, timeout=None, service_args=[]):
       self.logger = getLogger(__name__)
       self.timeout = timeout

       chrome_options = Options()
       chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
       chrome_options.add_argument('--disable-gpu')
       chrome_options.add_argument('--no-sandbox')
       self.browser = webdriver.Chrome(chrome_options=chrome_options)
       self.browser.set_window_size(1400, 700)
       self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
       self.browser.quit()

    def process_request(self, request, spider):
        if request.url != 'https://www.aqistudy.cn/historydata/':
            self.browser.get(request.url)
            time.sleep(1)
            page_source = self.browser.page_source.encode('utf-8')
            return scrapy.http.HtmlResponse(url=request.url, body=page_source, encoding='utf-8', request=request)


class StockSpiderMiddleware(object):
    def __init__(self, timeout=None, service_args=[]):
       #self.logger = getLogger(__name__)
       self.timeout = timeout

       chrome_options = Options()
       chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
       chrome_options.add_argument('--disable-gpu')
       chrome_options.add_argument('--no-sandbox')
       self.browser = webdriver.Chrome(chrome_options=chrome_options)
       self.browser.set_window_size(1400, 700)
       #self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
       self.browser.quit()

    use_selenium_urls = [
        'https://cn.investing.com/equities/vietnam',
        'http://www.vgchartz.com/yearly/2014/Global/',
        'http://www.vgchartz.com/yearly/2015/Global/',
        'http://www.vgchartz.com/yearly/2016/Global/',
        'http://www.vgchartz.com/yearly/2017/Global/',
        'http://www.vgchartz.com/yearly/2018/Global/',
    ]
    def process_request(self, request, spider):
        if request.url in self.use_selenium_urls:
            #self.logger.debug('Selenium is starting')
            try:
                self.browser.get(request.url)
                #time.sleep(10)
                #selector = Select(self.browser.find_element_by_id('stocksFilter'))
                #selector.select_by_index(0)
                page_source = self.browser.page_source.encode('utf-8')
                return scrapy.http.HtmlResponse(url=request.url, body=page_source, encoding='utf-8', request=request)
            except TimeoutException:
                return scrapy.http.HtmlResponse(url=request.url, status=500, request=request)
#\!===========


class MyspiderprojectSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MyspiderprojectDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
