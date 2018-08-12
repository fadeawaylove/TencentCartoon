# -*- coding: utf-8 -*-

import scrapy
from ..items import TencentcartoonItem

class TencentCartoonSpider(scrapy.Spider):
	# 爬虫名
	name = "tencentcartoon"
	# 起始url
	start_urls = ["http://ac.qq.com/Comic/ComicInfo/id/547513"]
	# 允许域名
	allowed_domains = ["ac.qq.com"]
	# 主域名
	base_url = u"http://ac.qq.com"

	def parse(self, response):
		# 解析起始页面获取章节的a标签
		chapter_infos = response.xpath('//ol[@class="chapter-page-all works-chapter-list"]/li/p/span/a')
		# 获取小说的名字
		cartoon_name = response.xpath('//h2[@class="works-intro-title ui-left"]/strong/text()').extract_first()

		for chapter in chapter_infos[:2]:
			chapter_name = chapter.xpath("./@title").extract_first()
			chapter_url = chapter.xpath("./@href").extract_first()

			chapter_url = self.base_url + chapter_url
			yield scrapy.Request(url=chapter_url, meta = {"cartoon_name":cartoon_name,"chapter_name":chapter_name},callback=self.parse_page)

	def parse_page(self, response):
		"""
			解析具体页面，获取图片的链接
		"""
		# 获取所有图片的img标签
		img_list = response.xpath('//ul[@id="comicContain"]/li/img')
		for img in img_list:
			img_url = img.xpath("./@src").extract_first()
			img_num = img.xpath("./@data-pid").extract_first()

			# 会出现获取不到img_num的情况
			if img_num is None:
				img_num = img_url.split("_")[-1].split(".")[0]

			item = TencentcartoonItem()
			item["image_url"] = img_url
			item["image_num"] = img_num
			item["cartoon_name"] = response.meta["cartoon_name"]
			item["chapter_name"] = response.meta["chapter_name"]

			yield item



		



