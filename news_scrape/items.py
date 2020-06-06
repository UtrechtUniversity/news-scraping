# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsScrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    article_info = scrapy.Field()
    article_body = scrapy.Field()
    publication_date = scrapy.Field()
    publication_time = scrapy.Field()
    created_at = scrapy.Field()
    image = scrapy.Field()
    reactions = scrapy.Field()
    author = scrapy.Field()
    doctype = scrapy.Field()
    url = scrapy.Field()
    tags = scrapy.Field()
    twitter = scrapy.Field()
    facebook = scrapy.Field()
    iframe = scrapy.Field()
