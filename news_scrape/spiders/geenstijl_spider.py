import scrapy
import re
import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from ..items import NewsScrapeItem
# import logging


# logging.basicConfig(filename='geenstij.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
class GeenstijSpider(scrapy.Spider):
    """Scrapes Groenlinks"""

    name = 'geen'

    start_urls = ['https://www.geenstijl.nl/archieven/maandelijks/2020/05/']


    # function to remove html tags, used for cleaning footer
    TAG_RE = re.compile(r'<[^>]+>')

    def remove_tags(self, text):
        return self.TAG_RE.sub('', text)

   # function for removing extra \n and spaces, used in cleaning footer
    def clean(self, line):
        line = line.strip()
        line = re.sub("\n", "", line)
        line = re.sub("\xa0|", "", line)
        line = re.sub(" ", "", line)
        line = re.sub(",", "", line)
        return line

    # function for extracting date from the footer
    def date_func(self, text):
        date = re.findall(r'[0-9]{2}[-|\/]{1}[0-9]{2}[-|\/]{1}[0-9]{2}', text)
        return date

    # function for extracting time from the footer
    def time_func(self, text):
        time = re.findall(r'(?:[01]\d|2[0123]):(?:[012345]\d)', text)
        return time

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)

        article_page_linkss = response.xpath('//div[@class]/ul[@class]/li/a/@ href').getall()
        article_page_links = article_page_linkss[::-1]
        yield from response.follow_all(article_page_links, self.parse_article)
        # return [response.follow(start_url, self.parse_article) for start_url in article_page_links]


        # next_page = response.xpath("//a[@class='btn pull-right']/@href").get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)


    def parse_article(self, response):
        # def extract_with_xpath(query):
        #     return response.xpath(query).get()
        # return response.xpath(query).get(default='').strip()

        article_id = response.xpath("//div[@class='main_content col-xs-12 col-sm-7']/article/@id").get()

        title = response.xpath("//div[@class='col-xs-12']/h1/text()").get()

        article_info = response.xpath("//div[@class='article-intro']/p/text()").get()

        article_body = response.xpath("//div[@class='article_content']/p//text()").getall()
        article_body_str = ''.join(str(e) for e in article_body)

        footer = self.remove_tags(response.xpath("//div[@class='art-footer']/div[@class='col-xs-12 col-sm-7']").get())
        footer_clean = self.clean(footer)
        date = self.date_func(footer_clean)
        publication_date = ''.join(str(e) for e in date)

        time = self.time_func(footer_clean)
        publication_time = ''.join(str(e) for e in time)

        created_at = datetime.datetime.now()

        image = response.xpath("//div[@class='article_content']/*/img/@src").getall()
        if len(image) != 0:
            image_dict = {i: image[i] for i in range(0, len(image))}
            image_dict = str(image_dict)
        else:
            image_dict = None
        #
        # if len(image) == 0:
        #     image = 'None'

        reactions = response.xpath("//div[@class='col-xs-12 col-sm-7']/a[@id='comment-count']/text()").get()

        author = response.xpath("//div[@class='col-xs-12 col-sm-7']/a[1]/text()").get()

        doctype = 'geenstijl.nl'
        url = response.url

        tags_list = response.xpath("//ul[@class='art-tags']/li/a/text()").getall()
        tags = ', '.join(str(i) for i in tags_list)

        twitter = response.xpath("//div[@class='icon-twitter pull-left']/a/@href").get()
        facebook = response.xpath("//div[@class='icon-facebook pull-left']/a/@href").get()
        iframe = response.xpath("//iframe[@class='puu-video_frame']/@data-src").get()
        #
        items = NewsScrapeItem()
        items['article_id'] = article_id
        items['title'] = title
        items['article_info'] = article_info
        items['article_body'] = article_body_str
        items['publication_date'] = publication_date
        items['publication_time'] = publication_time
        items['created_at'] = created_at
        items['image'] = image_dict
        items['reactions'] = reactions
        items['author'] = author
        items['doctype'] = doctype
        items['url'] = url
        items['tags'] = tags
        items['twitter'] = twitter
        items['facebook'] = facebook
        items['iframe'] = iframe

        yield items

class DatabasePipeline(object):

    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    def process_item(self, item, spider):
        return item


## TODO: 1- scrape in order
## TODO: 2- iframes
