import scrapy
import re
import datetime

class GeenstijSpider(scrapy.Spider):
    name = "geenstijl"
    TAG_RE = re.compile(r'<[^>]+>')
    start_urls = [
        'https://www.geenstijl.nl/',
    ]

    # function for removing html tags
    def remove_tags(self, text):
        return self.TAG_RE.sub('', text)

    def parse(self, response):
        for news in response.xpath("//article[@id]"):

            yield {
                'article_id': news.css('article').attrib['id'],
                'body': self.remove_tags(news.xpath("div[@class='col-xs-12']/div[@class='article_content']").extract_first()),
                'title': news.xpath("div[@class='col-xs-12']/h1/a/text()").extract_first(),
                'footer': self.remove_tags(news.xpath("div[@class='art-footer']/div[@class='col-xs-12 col-sm-7']").extract_first()),
                'created_at': datetime.datetime.now(),
                'image': news.xpath("div[@class='col-xs-12']/div[@class='article_content']/p[@class='puu-vsl']/img/@src").extract_first(),
                'reactions': news.xpath("div[@class='art-footer']/div[@class='col-xs-12 col-sm-7']/a[@id='comment-count']/text()").extract_first()[0:2],
                'author': news.xpath("div[@class='art-footer']/div[@class='col-xs-12 col-sm-7']/a[1]/text()").extract_first(),

            }