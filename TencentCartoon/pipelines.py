# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline  # 提供的专门下载图片的类
import scrapy
import os
from settings import IMAGES_STORE
import json

class TencentcartoonPipeline(ImagesPipeline):

	# 这个函数可以获取图片的请求信息,返回值是下载图片的url的request对象
    def get_media_requests(self, item, info):
    	yield scrapy.Request(item['image_url'])

    # 处理item完毕的方法，做收尾工作
    def item_completed(self, result, item, info):
    	"""
    		result:图片下载结果 
    		[(True, {'url': 'https://manhua.qpic.cn/manhua_detail/0/19_09_11_3c61a215926edb887e43820bcbb307bc_3421.jpg/0', 'path': 'full/43b4b8f5ee01001456a0d4c5ef3c27036c84e85e.jpg', 'checksum': '2c676909ba2463f900d1799f060943ac'})]    		
    	"""
    	base_dir = IMAGES_STORE 
    	# 文件夹的名字
    	old_path = base_dir + "/" + result[0][1]["path"]
    	# 创建新的文件夹
    	new_dir = base_dir + "/" + item["cartoon_name"] + '/' + item["chapter_name"]
    	if not os.path.exists(new_dir):
    		os.makedirs(new_dir)

    	new_path = new_dir + "/" + str(item["image_num"]) + '.jpg'
    	os.rename(old_path, new_path)

    	print("新的保存路径：")
    	print(new_path)
    	item["image_path"] = new_path
    	return item

class SaveJsonPipeline(object):
	"""这个管道把item信息保存到json文件中"""

	def open_spider(self, spider):
		self.file = open(IMAGES_STORE + "/" + "manhua.json", 'w')

	def process_item(self, item, spider):
		json_data = json.dumps(dict(item)) + ',\n'

		self.file.write(json_data)
		return item


	def close_spider(self, spider):
		self.file.close()





