# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
import scrapy
from scrapy.http import HtmlResponse
import time


class TencentDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    # 自定义腾讯动漫的下载中间件，等待页面中的图片链接加载完毕
    def __init__(self):
        self.driver = webdriver.Chrome()

    def process_request(self, request, spider):
        if "cid" in request.url:
            print("获取页面内容中：%s" % request.url)
            # 重写处理请求的中间件，返回一个response对象
            self.driver.get(request.url)

            # 获取有多少个图片
            imgs = self.driver.find_elements_by_xpath('//ul[@id="comicContain"]/li/img')
            for i in range(len(imgs)):
                # 向下滚动到底部，加载所有的图片url
                js = 'window.scrollTo(800,' + str((i+1) * 1280) + ')'
                self.driver.execute_script(js) 
                time.sleep(2)
            html = self.driver.page_source
            
            return HtmlResponse(url=self.driver.current_url,
                                body=html.encode("utf-8"),
                                encoding="utf-8",
                                request=request
                                )
    def __del__(self):
        self.driver.quit()
