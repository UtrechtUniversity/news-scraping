from scrapy.spiders import SitemapSpider
from ..items import NewsScrapeItem
import re
import datetime
import logging
from scrapy.utils.log import configure_logging

# configure_logging(install_root_handler=False)
# logging.basicConfig(
#     filename='log_error.txt',
#     filemode = 'a',
#     format='%(levelname)s: %(message)s',
#     level=logging.ERROR
# )

logging.basicConfig(
    filename='log.txt',
    format='%(asctime)s: %(levelname)s: %(message)s',
    level=logging.ERROR
)


class NuSpider(SitemapSpider):
    name = 'nu'
    sitemap_urls = ['https://www.nu.nl/sitemap_news.xml']
    TAG_RE = re.compile(r'<[^>]+>')

    # def __init__(self, *args, **kwargs):
    #     logger = logging.getLogger('scrapy.spidermiddlewares.httperror')
    #     logger.setLevel(logging.ERROR)
    #     super().__init__(*args, **kwargs)

    # Function for removing newline tags, used in cleaning news body
    def clean(self, line):
        line = line.strip()
        line = re.sub("\n", "", line)
        return line

    # Function for removing html tags, used in cleaning news body

    def remove_tags(self, text):
        return self.TAG_RE.sub(' ', text)

    def parse(self, response):
        logging.info('Parse function called on %s', response.url)
        if response.url.split('/')[-2] == 'video':
            pass
        else:
            # Extract article unique id
            try:
                id = response.url.split('/')[-2]
            except AttributeError:
                id = None

            try:
                title = response.xpath("//h1[@class]/text()").extract_first()
            except AttributeError:
                title = None

            try:
                teaser = None
            except AttributeError:
                teaser = None

            try:
                article_body = response.xpath("//div[@class='block-content']/p | //div[@class='block-content']/h2"
                                              " | //div[@class='block-content']/h3| //div[@class='inner']").extract()
                # article_body = response.xpath("//div[@id]/div[@class='block-wrapper']/div[@class='block-content']//text()["
                #                               "not(ancestor::span)]").extract()
                article_body_str = ''.join(str(e) for e in article_body)
                text = self.clean(article_body_str)
                text = self.remove_tags(text)
            except AttributeError:
                text = None

            try:
                category = response.xpath("//body/@data-section").extract_first()
            except AttributeError:
                category = None

            try:
                date_time = response.xpath("//span[@class='pubdate large']/text()").extract_first()
                publication_date = date_time[:-6]
            except AttributeError:
                publication_date = None

            try:
                publication_time = date_time[-6:]
            except AttributeError:
                publication_time = None

            try:
                created_at = datetime.datetime.now()
            except AttributeError:
                created_at = None

            try:
                header_image = response.xpath("//*[@id]/div/div/div[1]/figure/img/@data-src").extract()
                image_list = response.xpath("//div[@class='block-image']/img[@class='lazy-unveil']/@data-src").extract()
                images = image_list + header_image
                if len(images) != 0:
                    image_dict = {i: images[i] for i in range(0, len(images))}
                    image_dict = str(image_dict)
                else:
                    image_dict = None
            except AttributeError:
                image_dict = None

            try:
                reactions = response.xpath("//div/div/span/a/span/text()").extract_first()
            except AttributeError:
                reactions = None

            try:
                author_name = response.xpath("//span[@class='author']/text()").extract_first()
                author = self.clean(author_name)
            except AttributeError:
                author = None

            doctype = 'nu.nl'

            try:
                url = response.url
            except AttributeError:
                url = None

            try:
                tags_list = response.xpath("//div[@class='tags']/a[@class]/span/text()").extract()
                tags = ', '.join(str(i) for i in tags_list)
            except AttributeError:
                tags = None

            sitemap_url = "https://www.nu.nl/sitemap_news.xml"

            items = NewsScrapeItem()
            items['id'] = id  # 1- unique id
            items['url'] = url  # 2- source url of the item
            items['text'] = text  # 3- The full text of the document
            items['tags'] = tags  # 4- list of tags
            items['title'] = title  # 5- title of the document
            items['teaser'] = teaser  # 6- some short paragraph between title and text if any
            items['author'] = author  # 7- journalist's name
            items['doctype'] = doctype  # 8- source of the document
            items['category'] = category  # 9- news section if any
            items['images'] = image_dict  # 10- dictionary of images
            items['reactions'] = reactions  # 11- number of reactions
            items['created_at'] = created_at  # 12- date and time of scraping
            items['sitemap_url'] = sitemap_url  # 13- url of feed if any
            items['publication_date'] = publication_date  # 14- date of publication
            items['publication_time'] = publication_time  # 15- time of publication

            yield items


class DatabasePipeline(object):

    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    def process_item(self, item, spider):
        return item
