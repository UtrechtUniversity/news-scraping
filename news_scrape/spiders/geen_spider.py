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
    name = 'geenstijl'
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

        # *** Extract article's unique id ***
        try:
            id = response.xpath("//div[@class='main_content col-xs-12 col-sm-7']/article/@id").get()
        except AttributeError:
            id = None

        # *** Extract news title ***
        try:
            title = response.xpath("//div[@class='col-xs-12']/h1/text()").get()
        except AttributeError:
            title = None

        # *** Extract teaser- A short abstract between title and body ***
        try:
            teaser = response.xpath("//div[@class='article-intro']/p/text()").get()
        except AttributeError:
            teaser = None

        # *** Extract article body ***
        try:
            article_body = response.xpath("//div[@class='article_content']/p//text()").getall()
            text = ''.join(str(e) for e in article_body)
        except AttributeError:
            text = None

        # *** There is no article category for geenstijl articles ***
        category = None

        # *** Extract publication date and time ***
        try:
            # Extract footer
            footer = self.remove_tags(response.xpath("//div[@class='art-footer']/div[@class='col-xs-12 col-sm-7']").get())
            footer_clean = self.clean(footer)
            # Extract date
            date = self.date_func(footer_clean)
            date_str = ''.join(str(e) for e in date)
            publication_date = datetime.datetime.strptime(date_str, '%d-%m-%y')
            publication_date = publication_date.date()
            d = publication_date.strftime("%Y-%m-%d")
            # Extract time
            time = self.time_func(footer_clean)
            time_str = ''.join(str(e) for e in time)
            publication_time = datetime.datetime.strptime(time_str, '%H:%M')
            publication_time = publication_time.time()
            t = publication_time.strftime("%H:%M:%S")
            # Join date and time and change type to datetime
            date_time = d + ' ' + t
            publication_date_time = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        except AttributeError:
            publication_date_time = None

        # *** Extract scraping date and time ***
        try:
            created_at = datetime.datetime.now()
        except AttributeError:
            created_at = None

        # *** Extract link to images ***
        try:
            images = response.xpath("//div[@class='article_content']/*/img/@src").getall()
            if len(images) != 0:
                image_dict = {i: images[i] for i in range(0, len(images))}
                image_dict = str(image_dict)
            else:
                image_dict = None
        except AttributeError:
            image_dict = None

        # *** Extract number of reactions to the article ***
        try:
            reactions = response.xpath("//div[@class='col-xs-12 col-sm-7']/a[@id='comment-count']/text()").get()
        except AttributeError:
            reactions = None

        # *** Extract author name ***
        try:
            author = response.xpath("//div[@class='col-xs-12 col-sm-7']/a[1]/text()").get()
        except AttributeError:
            author = None

        # *** News resource ***
        doctype = 'geenstijl.nl'

        # *** News URL ***
        try:
            url = response.url
        except AttributeError:
            url = None

        # *** Extract tags ***
        try:
            tags_list = response.xpath("//ul[@class='art-tags']/li/a/text()").getall()
            tags = ', '.join(str(i) for i in tags_list)
        except AttributeError:
            tags = None

        # *** Most updated news are extracted from sitemap, this is the link to the nu.nl sitemap ***
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
        items['sitemap_url'] = sitemap_url              # 13- url of feed if any
        items['publication_date_time'] = publication_date_time    # 14- date and time of publication

        yield items


class DatabasePipeline(object):

    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    def process_item(self, item, spider):
        return item

