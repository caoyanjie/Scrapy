# -*- coding: utf-8 -*-
import scrapy

from scrapy.http.cookies import CookieJar
import time

from selenium import webdriver


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['scrapybook.com']
    login_url = 'http://examples.scrapybook.com/post/nonce.php'
    request_url = 'http://examples.scrapybook.com/post/nonce-login.php'
    home_page_url = 'http://examples.scrapybook.com/post/data.php'
    start_urls = [login_url]
    #cookie_jar = CookieJar()

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'MySpiderProject.middlewares.LoginScrapyBook': 543}
    }

    '''
    def start_requests(self):
        options = webdriver.chrome.options.Options()
        options.add_argument('--headless')
        browser = webdriver.Chrome(options=options)

        browser.get(self.login_url)
        browser.find_element_by_xpath('//input[@name="user"]').send_keys('user')
        browser.find_element_by_xpath('//input[@name="pass"]').send_keys('pass')
        browser.find_element_by_xpath('//input[@name="commit"]').click()
        time.sleep(2)

        # 获得cookies
        cookies = browser.get_cookies()
        print(cookies)
        browser.close()

        #yield scrapy.FormRequest(url, cookies=cookies, callback=self.parse_page)
        return [scrapy.Request(self.home_page_url, cookies=cookies)]
        #return [scrapy.Request(url=self.home_page_url)]
    '''

    def parse(self, response):
        '''
        form_data = {
            'user': 'user',
            'pass': 'pass',
            'commit': 'Login',
            'nonce': response.xpath('//input[@name="nonce"]/@value').extract()
        }

        return scrapy.http.FormRequest(self.request_url, formdata=form_data, callback=self.check_login)
        '''

        print(f'>>>>>>>>>> login result:                    {response.xpath("//h1/text()").extract()}')
        print(f'>>>>>>>>>> response.request.headers.cookie: {response.request.headers.getlist("Cookie")}')
        print(f'>>>>>>>>>> response.request.cookies:        {response.request.cookies}')
        print(f'>>>>>>>>>> response.headers.Set-Cookie:     {response.headers.getlist("Set-Cookie")}')
        #print(f'>>>>>>>>>> extract_cookie:                  {self.cookie_jar.extract_cookies(response, response.request)}')
        print()
        time.sleep(1)
        #return scrapy.Request(self.home_page_url, cookies=response.request.meta['cookies'], callback=self.check_login)
        return scrapy.Request(self.home_page_url, cookies=response.request.cookies, callback=self.check_login, dont_filter=True)
        return scrapy.Request(self.home_page_url, callback=self.check_login, dont_filter=True)

    def check_login(self, response):
        print(f'>>>>>>>>>> login result:                    {response.xpath("//h1/text()").extract()}')
        print(f'>>>>>>>>>> response.request.headers.cookie: {response.request.headers.getlist("Cookie")}')
        print(f'>>>>>>>>>> response.request.cookies:        {response.request.cookies}')
        print(f'>>>>>>>>>> response.headers.Set-Cookie:     {response.headers.getlist("Set-Cookie")}')
        print()
        #print(f'>>>>>>>>>> extract_cookie:                  {self.cookie_jar.extract_cookies(response, response.request)}')
        return scrapy.Request(self.home_page_url, callback=self.recheck, dont_filter=True)

    def recheck(self, response):
        print(f'>>>>>>>>>> login result:                    {response.xpath("//h1/text()").extract()}')
        print(f'>>>>>>>>>> response.request.headers.cookie: {response.request.headers.getlist("Cookie")}')
        print(f'>>>>>>>>>> response.request.cookies:        {response.request.cookies}')
        print(f'>>>>>>>>>> response.headers.Set-Cookie:     {response.headers.getlist("Set-Cookie")}')
        #print(f'>>>>>>>>>> extract_cookie:                  {self.cookie_jar.extract_cookies(response, response.request)}')
        print()

