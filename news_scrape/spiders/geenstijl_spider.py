import scrapy
import re
import datetime
from ..items import NewsScrapeItem
import logging

# logging.basicConfig(filename='geenstij.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

class GeenstijSpider(scrapy.Spider):
    name = 'geenstijl'

    start_urls = ['https://www.geenstijl.nl/']
    # start_urls = ['https://www.geenstijl.nl/archieven/maandelijks/2020/05/']

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

    # function for extracting time and date from footer

    def date_func(self, text):
        date = re.findall(r'[0-9]{2}[-|\/]{1}[0-9]{2}[-|\/]{1}[0-9]{2}', text)
        return date

    def time_func(self, text):
        time = re.findall(r'(?:[01]\d|2[0123]):(?:[012345]\d)', text)
        return time

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)

        article_page_linkss = response.xpath('//li/a/@href')
        article_page_links = article_page_linkss[::-1]
        yield from response.follow_all(article_page_links, self.parse_article)

        # next_page = response.xpath("//a[@class='btn pull-right']/@href").get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)


    def parse_article(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).get()
            # return response.xpath(query).get(default='').strip()

        title = extract_with_xpath("//div[@class='col-xs-12']/h1/text()")

        article_info = extract_with_xpath("//div[@class='article-intro']/p/text()")

        article_body= response.xpath("//div[@class='article_content']/p//text()").getall()
        article_body_str = ''.join(str(e) for e in article_body)

        footer= self.remove_tags(extract_with_xpath("//div[@class='art-footer']/div[@class='col-xs-12 col-sm-7']"))
        footer_clean = self.clean(footer)
        date = self.date_func(footer_clean)
        publication_date = ''.join(str(e) for e in date)
        time = self.time_func(footer_clean)
        publication_time= ''.join(str(e) for e in time)

        created_at = datetime.datetime.now()
        try:
            image = response.xpath("//div[@class='article_content']/*/img/@src").getall()
        except:
            print("title:", title, "Oops!  That was no valid number.  Try again...")
        reactions = extract_with_xpath("//div[@class='col-xs-12 col-sm-7']/a[@id='comment-count']/text()")
        author = extract_with_xpath("//div[@class='col-xs-12 col-sm-7']/a[1]/text()")
        doctype = 'geenstijl.nl'
        url = response.url
        tags_list = response.xpath("//ul[@class='art-tags']/li/a/text()").getall()
        tags =', '.join(str(i) for i in tags_list)

        twitter = extract_with_xpath("//div[@class='icon-twitter pull-left']/a/@href")
        facebook = extract_with_xpath("//div[@class='icon-facebook pull-left']/a/@href")
        iframe = response.xpath("//iframe[@class='puu-video_frame']/@data-src").get()
        #
        items = NewsScrapeItem()
        items['title'] = title
        items['article_info'] = article_info
        items['article_body'] = article_body_str
        items['publication_date'] = publication_date
        items['publication_time'] = publication_time
        items['created_at'] = created_at
        items['image'] = image
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

