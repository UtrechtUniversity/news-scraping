from scrapy.spiders import SitemapSpider
from ..items import NewsScrapeItem
import re
import datetime
import logging


logging.basicConfig(
    filename='log.txt',
    format='%(asctime)s: %(levelname)s: %(message)s',
    level=logging.ERROR
)


class NuSpider(SitemapSpider):
    name = 'nu'
    sitemap_urls = ['https://www.nu.nl/sitemap_news.xml']
    TAG_RE = re.compile(r'<[^>]+>')

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
        # Skip pages containing video without text
        if response.url.split('/')[-2] == 'video':
            pass
        else:
            # *** Extract article's unique id ***
            try:
                id = response.url.split('/')[-2]
            except AttributeError:
                id = None

            # *** Extract news title ***
            try:
                title = response.xpath("//h1[@class]/text()").extract_first()
            except AttributeError:
                title = None

            # *** Extract teaser- A short abstract between title and body ***
            try:
                teaser = response.xpath("//p[@class='excerpt']/text()").extract_first()
            except AttributeError:
                teaser = None

            # *** Extract article body ***
            try:
                article_body = response.xpath("//div[@class='block-content']/p | //div[@class='block-content']/h2"
                                              " | //div[@class='block-content']/h3| //div[@class='inner']").extract()

                article_body_str = ''.join(str(e) for e in article_body)
                text = self.clean(article_body_str)
                text = self.remove_tags(text)
            except AttributeError:
                text = None

            # *** Extract article category ***
            try:
                category = response.xpath("//body/@data-section").extract_first()
            except AttributeError:
                category = None

            # *** Extract publication date and time ***
            try:
                date_time = response.xpath("//span[@class='pubdate large']/text()").extract_first()
                # Turn Dutch month to English month name
                date_time = date_time.replace('januari', 'january')
                date_time = date_time.replace('februari', 'february')
                date_time = date_time.replace('maart', 'march')
                date_time = date_time.replace('mei', 'may')
                date_time = date_time.replace('juni', 'june')
                date_time = date_time.replace('juli', 'july')
                date_time = date_time.replace('augustus', 'august')
                date_time = date_time.replace('oktober', 'october')
                publication_date_time = datetime.datetime.strptime(date_time, "%d %B %Y %H:%M")

            except AttributeError:
                publication_date_time = None

            # *** Extract scraping date and time ***
            try:
                created_at = datetime.datetime.now()
            except AttributeError:
                created_at = None

            # *** Extract link to images ***
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

            # *** Extract number of reactions to the article ***
            try:
                reactions = response.xpath("//div/div/span/a/span/text()").extract_first()
            except AttributeError:
                reactions = None

            # *** Extract author name ***
            try:
                author_name = response.xpath("//span[@class='author']/text()").extract_first()
                author = self.clean(author_name)
            except AttributeError:
                author = None

            # *** News resource ***
            doctype = 'nu.nl'

            # *** News URL ***
            try:
                url = response.url
            except AttributeError:
                url = None

            # *** Extract tags ***
            try:
                tags_list = response.xpath("//div[@class='tags']/a[@class]/span/text()").extract()
                tags = ', '.join(str(i) for i in tags_list)
            except AttributeError:
                tags = None

            # *** Most updated news are extracted from sitemap, this is the link to the nu.nl sitemap ***
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
            items['publication_date_time'] = publication_date_time  # 14- date and time of publication

            yield items


class DatabasePipeline(object):

    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    def process_item(self, item, spider):
        return item
