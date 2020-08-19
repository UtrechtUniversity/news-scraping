from scrapy.spiders import SitemapSpider
from ..items import NewsScrapeItem
import re
import datetime
import logging


# logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='log.txt',
    format='%(asctime)s: %(levelname)s: %(message)s',
    level=logging.ERROR
)

class GeenstijlSpider(SitemapSpider):
    name = 'geenstijq'
    sitemap_urls = ['https://www.geenstijl.nl/sitemap.xml']

    TAG_RE = re.compile(r'<[^>]+>')

    # Function for removing html tags, used in cleaning news body
    def remove_tags(self, text):
        return self.TAG_RE.sub('', text)

    # Function for removing extra \n and spaces, used in cleaning footer
    def clean(self, line):
        line = line.strip()
        line = re.sub("\n", "", line)
        line = re.sub("\xa0|", "", line)
        line = re.sub(" ", "", line)
        line = re.sub(",", "", line)
        return line

    # Function for extracting date from the footer
    def date_func(self, text):
        date = re.findall(r'[0-9]{2}[-|\/]{1}[0-9]{2}[-|\/]{1}[0-9]{2}', text)
        return date

    # Function for extracting time from the footer
    def time_func(self, text):
        time = re.findall(r'(?:[01]\d|2[0123]):(?:[012345]\d)', text)
        return time

    def parse(self, response):
        logging.info('Parse function called on %s', response.url)

        id = response.xpath("//div[@class='main_content col-xs-12 col-sm-7']/article/@id").get()

        title = response.xpath("//div[@class='col-xs-12']/h1/text()").get()

        teaser = response.xpath("//div[@class='article-intro']/p/text()").get()

        article_body = response.xpath("//div[@class='article_content']/p//text()").getall()
        text = ''.join(str(e) for e in article_body)

        category = None

        footer = self.remove_tags(response.xpath("//div[@class='art-footer']/div[@class='col-xs-12 col-sm-7']").get())
        footer_clean = self.clean(footer)
        date = self.date_func(footer_clean)
        publication_date = ''.join(str(e) for e in date)

        time = self.time_func(footer_clean)
        publication_time = ''.join(str(e) for e in time)

        created_at = datetime.datetime.now()

        images = response.xpath("//div[@class='article_content']/*/img/@src").getall()
        if len(images) != 0:
            image_dict = {i: images[i] for i in range(0, len(images))}
            image_dict = str(image_dict)
        else:
            image_dict = None


        reactions = response.xpath("//div[@class='col-xs-12 col-sm-7']/a[@id='comment-count']/text()").get()

        author = response.xpath("//div[@class='col-xs-12 col-sm-7']/a[1]/text()").get()

        doctype = 'geenstijl.nl'

        url = response.url

        tags_list = response.xpath("//ul[@class='art-tags']/li/a/text()").getall()
        tags = ', '.join(str(i) for i in tags_list)

        sitemap_url = "https://www.geenstijl.nl/sitemap.xml"


        items = NewsScrapeItem()
        items['id'] = id                                # 1- unique id
        items['url'] = url                              # 2- source url of the item
        items['text'] = text                            # 3- The full text of the document
        items['tags'] = tags                            # 4- list of tags
        items['title'] = title                          # 5- title of the document
        items['teaser'] = teaser                        # 6- some short paragraph between title and text if any
        items['author'] = author                        # 7- journalist's name
        items['doctype'] = doctype                      # 8- source of the document
        items['category'] = category                    # 9- news section if any
        items['images'] = image_dict                    # 10- dictionary of images
        items['reactions'] = reactions                  # 11- number of reactions
        items['created_at'] = created_at                # 12- date and time of scraping
        # items['htmlsource'] = htmlsource                # 13- the raw html code
        items['sitemap_url'] = sitemap_url              # 14- url of feed if any
        items['publication_date'] = publication_date    # 15- date of publication
        items['publication_time'] = publication_time    # 16- time of publication

        yield items

class DatabasePipeline(object):

    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    def process_item(self, item, spider):
        return item

