# -*- coding: utf-8 -*-
import scrapy

from scrapy.http import Request, FormRequest

from scrapy.http.cookies import CookieJar


class LoginTeambitionSpider(scrapy.Spider):
    name = 'login_teambition'
    login_url = 'https://account.teambition.com/login'
    request_login_url = 'https://account.teambition.com/api/login/phone'
    allowed_domains = ['teambition.com']
    cookie_jar = CookieJar()
    start_urls = [
        login_url
    ]

    #custom_settings = {
    #    'DOWNLOADER_MIDDLEWARES': {'MySpiderProject.middlewares.DelayLoading': 543}
    #}

    def parse(self, response):
        form_data = {
            'phone': '17521092026',
            'email': '17521092026',
            'password': 'qgdi2018Q',
            #'next_url': response.xpath('//div[@class="tb-auth third-bind-hide"]/a[2]/@href').extract(),
            'response_type': 'session',
            'token': response.xpath('//script[@id="secrets"]/@data-clienttoken').extract(),
            'client_id': response.xpath('//script[@id="secrets"]/@data-clientid').extract()
        }
        return [
            #FormRequest(self.request_login_url, formdata=form_data, callback=self.parse_welcome, meta = {'dont_merge_cookies': True, 'cookiejar': cookie_jar})
            FormRequest(self.request_login_url, formdata=form_data, callback=self.check_login)
        ]

    def check_login(self, response):
        #print(response.meta['cookiejar'])
        mine = response.xpath('//div[@class="item__3Uri item-my__3oKQ"]/span/text()').extract()
        notloging = response.xpath('//h1/text()').extract()
        print(f'>>>>>>>>>> mine: {mine} <<<<<<<<<<<<')
        print(f'>>>>>>>>>> notloging: {notloging} <<<<<<<<<<<')
        print(f'>>>>>>>>>> extract_cookie: {self.cookie_jar.extract_cookies(response, response.request)} <<<<<<<<<<')
        print(f'>>>>>>>>>> response.cookie: {response.request.headers.getlist("Cookie")} <<<<<<<<<<<')
        print(f'>>>>>>>>>> Set-Cookie: {response.headers.getlist("Set-Cookie")} <<<<<<<<<<<<')
        #yield Request('https://www.teambition.com/organization/5c3fb994f081fc0001d52d5b', callback=self.recheck)
        #return Request('https://www.teambition.com', callback=self.recheck)

    def recheck(self, response):
        mine = response.xpath('//div[@class="item__3Uri item-my__3oKQ"]/span/text()').extract()
        notloging = response.xpath('//h1/text()').extract()
        print('check!!!!!!!!!!!!!')
        print(f'mine: {mine}')
        print(f'notloging: {notloging}')
        print('!!!!!!!!!!!!!end')