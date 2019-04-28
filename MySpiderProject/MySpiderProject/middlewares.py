# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time


class AreaSpiderMiddleware(object):
    def __init__(self, timeout=None, service_args=[]):
       self.logger = getLogger(__name__)
       self.timeout = timeout

       browser_options = webdriver.FirefoxOptions()
       browser_options.add_argument('--headless')  # 使用无头浏览器模式
       browser_options.add_argument('--disable-gpu')
       browser_options.add_argument('--no-sandbox')
       self.browser = webdriver.Firefox(options=browser_options)
       self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
       self.browser.quit()

    def process_request(self, request, spider):
        if request.url != 'https://www.aqistudy.cn/historydata/':
            self.browser.get(request.url)
            time.sleep(1)
            page_source = self.browser.page_source.encode('utf-8')
            return scrapy.http.HtmlResponse(url=request.url, body=page_source, encoding='utf-8', request=request)


# \!################# login class basic ##################
class SeleniumLogin(object):
    login_urls = []
    form_params = {}    # key: html_input_tag_xpath; value: html_input_tag_value
    lognin_button_xpath = None
    browser_headless = True

    def __init__(self, timeout=None, service_args=[]):
        self.timeout = time
        browser_options = webdriver.FirefoxOptions()
        if self.browser_headless:
            browser_options.add_argument('--headless')  # 使用无头浏览器模式
        self.browser = webdriver.Firefox(options=browser_options)

    def __del__(self):
        self.browser.quit()

    def process_request(self, request, spider):
        #use_selenium = request.meta.get('use_selenium', False)
        if request.url not in self.login_urls:# or not use_selenium:
            return

        #self.logger.debug('Selenium is starting')
        try:
            self.browser.get(request.url)

            # 登录
            for key, value in self.form_params.items():
                self.browser.find_element(By.XPATH, key).send_keys(value)
                time.sleep(0.5)
            self.browser.find_element(By.XPATH, self.lognin_button_xpath).click()
            time.sleep(1)

            # 设置cookie
            self.set_selenium_cookie_to_scrapy(request)

            page_source = self.browser.page_source.encode('utf-8')
            return scrapy.http.HtmlResponse(url=request.url, body=page_source, encoding='utf-8', request=request)
        except TimeoutException:
            return scrapy.http.HtmlResponse(url=request.url, status=500, request=request)

    def set_selenium_cookie_to_scrapy(self, request):
        selenium_cookies = self.browser.get_cookies()
        new_cookies = {}
        for cookie_dict in selenium_cookies:
            new_cookies[cookie_dict['name']] = cookie_dict['value']
        request.cookies = new_cookies


# \!################# login some website #################
class LoginScrapyBook(SeleniumLogin):
    login_urls = ['http://examples.scrapybook.com/post/nonce.php']
    form_params = {
        '//input[@name="user"]': 'user',
        '//input[@name="pass"]': 'pass'
    }
    lognin_button_xpath = '//input[@name="commit"]'


# \!############## delay loading to load javascript ###############
class DelayLoading(object):
    use_selenium_urls = [
        'https://cn.investing.com/equities/vietnam',
        'http://www.vgchartz.com/yearly/2014/Global/',
        'http://www.vgchartz.com/yearly/2015/Global/',
        'http://www.vgchartz.com/yearly/2016/Global/',
        'http://www.vgchartz.com/yearly/2017/Global/',
        'http://www.vgchartz.com/yearly/2018/Global/',
        'https://www.teambition.com',
        'https://www.teambition.com/organization/5c3fb994f081fc0001d52d5b',
        'http://examples.scrapybook.com/post/data.php',
    ]

    def __init__(self, timeout=None, service_args=[]):
        self.timeout = time
        chrome_options = Options()
        #chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.set_window_size(1400, 700)

    def __del__(self):
        #self.browser.quit()
        pass

    def process_request(self, request, spider):
        if request.url not in self.use_selenium_urls:
            return

        print(f'>>>>>>>>>> request.headers.cookie: {request.headers.getlist("Cookie")} <<<<<<<<<<')
        print(f'>>>>>>>>>> request.cookie: {request.cookies} <<<<<<<<<<')
        if 'cookiejar' in request.meta:
            print(f'>>>>>>>>>> request.meta["cookiejar"]: {request.meta["cookiejar"]} <<<<<<<<<<')

        self.set_scrapy_cookie_to_selenium(request)
        #self.logger.debug('Selenium is starting')
        try:
            time.sleep(10)
            print('获取哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈')
            self.browser.get(request.url)
            #time.sleep(10)
            #selector = Select(self.browser.find_element_by_id('stocksFilter'))
            #selector.select_by_index(0)
            page_source = self.browser.page_source.encode('utf-8')
            return scrapy.http.HtmlResponse(url=request.url, body=page_source, encoding='utf-8', request=request)
        except TimeoutException:
            return scrapy.http.HtmlResponse(url=request.url, status=500, request=request)

    def set_selenium_cookie_to_scrapy(self, request):
        seleniumCookies = self.browser.get_cookies()
        cookie = [f'{item["name"]}:{item["value"]}' for item in seleniumCookies]
        cookMap = {}
        for elem in cookie:
            str = elem.split(':')
            cookMap[str[0]] = str[1]
        request.cookies = cookMap

    def set_scrapy_cookie_to_selenium(self, request):
        scrapy_cookie = request.headers.getlist('Cookie')
        new_cookie = {}
        for cookie in scrapy_cookie:
            cookie = cookie.decode()
            cookie_items = cookie.split(';')
            for cookie_item in cookie_items:
                items = cookie_item.strip().split('=')
                new_cookie[items[0].strip()] = items[1].strip()
        #print('↓' * 20)
        #print(new_cookie)
        #self.browser.add_cookie(new_cookie)
        #print(self.browser.get_cookies())
        #print('↑' * 20)
        print('获取哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈')
        self.browser.get(request.url)
        for key, value in new_cookie.items():
            self.browser.add_cookie({'name':key, 'value':value})


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
