# -*- coding: utf-8 -*-

import scrapy

class ArticleSpider(scrapy.Spider):
    name = 'article'

    def start_requests(self):
        urls = [
            "https://entertain.naver.com/home",
            "https://news.naver.com",
        ]
        return [scrapy.Request(url=url, callback=self.parse) for url in urls]

    def parse(self, response):
        url = response.url
        title = response.css('h1 a span::text').extract_first()
        print('URL is {}'.format(url))
        print('TITLE is {}'.format(title))
