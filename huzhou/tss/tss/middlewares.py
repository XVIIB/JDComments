# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from scrapy import signals
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


class TssSpiderMiddleware(object):
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


class TssDownloaderMiddleware(object):
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
        chrome_options = Options()
        chrome_options.add_argument(
            '--headless')  # 使用无头谷歌浏览器模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        # 指定谷歌浏览器路径
        self.driver = webdriver.Chrome(chrome_options=chrome_options,
                                       executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

        if request.url != 'https://item.jd.com/6494402.html':
            self.driver.get(request.url)
            page = request.meta.get('page', 1)
            # time.sleep(10)
            # //div[@class='ui-pager-next']

            # ///翻页///---------------------------------------------------------------------------
            # if page > 1:
            #     print("click", page)
            #     # element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="comment-0"]/div[13]/div/div/a[7]')))
            #     # element1 = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="comment-0"]/div[13]/div/div/a[8]')))
            #     element = self.driver.find_element_by_xpath('//*[@id="comment-0"]/div[13]/div/div/a[7]')
            #     element1 = self.driver.find_element_by_xpath('//*[@id="comment-0"]/div[13]/div/div/a[8]')
            #     self.driver.execute_script("arguments[0].click();", element)
            #     for i in range(0, page-2):
            #         self.driver.get(self.driver.current_url)
            #         self.driver.execute_script("arguments[0].click();", element1)
            # else:
            #     # element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="comment-0"]/div[13]/div/div/a[7]')))
            #     element = self.driver.find_element_by_xpath('//*[@id="comment-0"]/div[13]/div/div/a[7]')
            #     self.driver.execute_script("arguments[0].click();", element)
            # ///结束///------------------------------------------------------------------
            url = self.driver.current_url
            html = self.driver.page_source
            self.driver.quit()
            return scrapy.http.HtmlResponse(url=url, body=html.encode('utf-8'), encoding='utf-8', request=request)
        else:
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
