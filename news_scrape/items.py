# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsScrapeItem(scrapy.Item):
    # fields for the item
    id = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    tags = scrapy.Field()
    title = scrapy.Field()
    teaser = scrapy.Field()
    author = scrapy.Field()
    doctype = scrapy.Field()
    category = scrapy.Field()
    images = scrapy.Field()
    reactions = scrapy.Field()
    created_at = scrapy.Field()
    htmlsource = scrapy.Field()
    sitemap_url = scrapy.Field()
    publication_date_time = scrapy.Field()
    # publication_time = scrapy.Field()
