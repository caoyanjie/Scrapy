# -*- coding: utf-8 -*-
import scrapy

from scrapy.http.cookies import CookieJar
import time


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['scrapybook.com']
    login_url = 'http://examples.scrapybook.com/post/nonce.php'
    request_url = 'http://examples.scrapybook.com/post/nonce-login.php'
    home_page_url = 'http://examples.scrapybook.com/post/data.php'
    start_urls = ['http://examples.scrapybook.com/post/nonce.php']
    cookie_jar = CookieJar()

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'MySpiderProject.middlewares.LoginScrapyBook': 543}
    }

    def parse(self, response):
        '''
        form_data = {
            'user': 'user',
            'pass': 'pass',
            'commit': 'Login',
            'nonce': response.xpath('//input[@name="nonce"]/@value').extract()
        }

        return [
            scrapy.http.FormRequest(self.request_url, formdata=form_data, callback=self.check_login)
        ]
        '''
        print(f'>>>>>>>>>> login result: {response.xpath("//h1/text()").extract()} <<<<<<<<<<<<<<<<<')
        print(f'>>>>>>>>>> extract_cookie: {self.cookie_jar.extract_cookies(response, response.request)} <<<<<<<<<<<<')
        print(f'>>>>>>>>>> response.request.headers.cookie: {response.request.headers.getlist("Cookie")} <<<<<<<<<<<')
        print(f'>>>>>>>>>> response.headers.Set-Cookie: {response.headers.getlist("Set-Cookie")} <<<<<<<<<<<<')
        print(f'>>>>>>>>>> request.cookies: {response.request.cookies} <<<<<<<<<<')
        print()
        time.sleep(3)
        return scrapy.Request(self.home_page_url, cookies=response.request.meta['cookies'], callback=self.check_login)

    def check_login(self, response):
        print(f'>>>>>>>>>> login result: {response.xpath("//h1/text()").extract()} <<<<<<<<<<<<<<<<<')
        print(f'>>>>>>>>>> extract_cookie: {self.cookie_jar.extract_cookies(response, response.request)} <<<<<<<<<<<<')
        print(f'>>>>>>>>>> response.request.headers.cookie: {response.request.headers.getlist("Cookie")} <<<<<<<<<<<')
        print(f'>>>>>>>>>> response.headers.Set-Cookie: {response.headers.getlist("Set-Cookie")} <<<<<<<<<<<<')
        print(f'>>>>>>>>>> request.cookies: {response.request.cookies} <<<<<<<<<<')
        #return scrapy.Request('http://examples.scrapybook.com/post/data.php')
