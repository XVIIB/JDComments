# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
# from tss.tss.items import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from tss.items import TssItem

chrome_options = Options()
chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
# 指定谷歌浏览器路径
driver = webdriver.Chrome(chrome_options=chrome_options,
                          executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')


class MydomainSpider(scrapy.Spider):
    name = 'mydomain'
    allowed_domains = ['item.jd.com']
    start_urls = ['https://item.jd.com/6494402.html#comment']

    def parse(self, response):
        print(response.xpath('//html'))
        for i in range(1, 2):
            yield scrapy.Request(response.url, callback=self.parse_items, meta={'page': i},dont_filter=True)

    def parse_items(self, response):
        print('parse_items')
        list = response.xpath('//*[@id="comment-0"]/div/div[2]/p/text()').extract()
        print(response.xpath('//*[@id="comment-0"]/div[13]/div/div/a[4]').extract())
        item = TssItem()
        tmp_str = ''
        for i in list:
            tmp_str = tmp_str + i
        item['commons'] = tmp_str
        yield {'item': item}


