# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentcartoonItem(scrapy.Item):
    
	# 图片的链接
    image_url = scrapy.Field()
    image_num = scrapy.Field()
    image_path = scrapy.Field()
    cartoon_name = scrapy.Field()
    chapter_name = scrapy.Field()

