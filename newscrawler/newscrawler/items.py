# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewscrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    blogger_name = scrapy.Field()
    art_tittle = scrapy.Field()
    art_subtittle = scrapy.Field()
    content_text = scrapy.Field()
    content_tags = scrapy.Field()
    bread_crum = scrapy.Field()
    key_page = scrapy.Field()
    url = scrapy.Field()
    pass
