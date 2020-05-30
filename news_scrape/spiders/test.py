import scrapy
import re
import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#
# TAG_RE = re.compile(r'<[^>]+>')
#
#
# def remove_tags(text):
#     return TAG_RE.sub('', text)

class NewsSpider(scrapy.Spider):
    name = 'news'

    start_urls = ['https://www.geenstijl.nl/']

    TAG_RE = re.compile(r'<[^>]+>')

    def remove_tags(self,text):
        return self.TAG_RE.sub('', text)

    def parse(self, response):
        author_page_linkss = response.xpath('//h1/a/@href')
        author_page_links = author_page_linkss[::-1]
        yield from response.follow_all(author_page_links, self.parse_author)

        # pagination_links = response.css('li.next a')
        # yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).get()
            # return response.xpath(query).get(default='').strip()

        yield {
            'title': extract_with_xpath("//div[@class='col-xs-12']/h1/text()"),
            'article_info': extract_with_xpath("//div[@class='article-intro']/p/text()"),
            # 'article_body': self.remove_tags(extract_with_xpath("//div[@class='article_content']/p")),
            'article_body': response.xpath("//div[@class='article_content']/p/text()").getall(),
            'footer': self.remove_tags(extract_with_xpath("//div[@class='art-footer']/div[@class='col-xs-12 col-sm-7']")),
            'created_at': datetime.datetime.now(),
            'image': response.xpath("//div[@class='article_content']/*/img/@src").getall(),
            'reactions': extract_with_xpath("//div[@class='col-xs-12 col-sm-7']/a[@id='comment-count']/text()"),
            'author': extract_with_xpath("//div[@class='col-xs-12 col-sm-7']/a[1]/text()"),
            'doctype': 'geenstijl.nl',
            'url': response.url,
            'tags': response.xpath("//ul[@class='art-tags']/li/a/text()").getall(),
            'twitter': extract_with_xpath("//div[@class='icon-twitter pull-left']/a/@href"),
            'facebook':extract_with_xpath("//div[@class='icon-facebook pull-left']/a/@href"),
            'iframe': response.xpath("//iframe[@class='puu-video_frame']/@data-src").get(),

        }