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

    # Function for removing newline tags, used in cleaning news body
    def clean(self, line):
        line = line.strip()
        line = re.sub("\n", "", line)
        return line



    def parse(self, response):
        logging.info('Parse function called on %s', response.url)

        id = response.url.split('/')[-2]

        title = response.xpath("//h1[@class]/text()").extract_first()

        teaser = None

        article_body = response.xpath("//div[@id]/div[@class='block-wrapper']/div[@class='block-content']//text()["
                                      "not(ancestor::span)]").extract()
        article_body_str = ''.join(str(e) for e in article_body)
        text = self.clean(article_body_str)

        category = response.xpath("//body/@data-section").extract_first()

        date_time = response.xpath("//span[@class='pubdate large']/text()").extract_first()
        publication_date = date_time[:-6]
        publication_time = date_time[-6:]

        created_at = datetime.datetime.now()

        header_image = response.xpath("//*[@id]/div/div/div[1]/figure/img/@data-src").extract()
        image_list = response.xpath("//div[@class='block-image']/img[@class='lazy-unveil']/@data-src").extract()
        images = image_list + header_image
        if len(images) != 0:
            image_dict = {i: images[i] for i in range(0, len(images))}
            image_dict = str(image_dict)
        else:
            image_dict = None

        reactions = response.xpath("//div/div/span/a/span/text()").extract_first()

        author_name = response.xpath("//span[@class='author']/text()").extract_first()
        author = self.clean(author_name)

        doctype = 'nu.nl'

        url = response.url

        tags_list = response.xpath("//div[@class='tags']/a[@class]/span/text()").extract()
        tags = ', '.join(str(i) for i in tags_list)

        sitemap_url = "https://www.nu.nl/sitemap_news.xml"



        items = NewsScrapeItem()
        items['id'] = id                              # 1- unique id
        items['url'] = url                            # 2- source url of the item
        items['text'] = text                          # 3- The full text of the document
        items['tags'] = tags                          # 4- list of tags
        items['title'] = title                        # 5- title of the document
        items['teaser'] = teaser                      # 6- some short paragraph between title and text if any
        items['author'] = author                      # 7- journalist's name
        items['doctype'] = doctype                    # 8- source of the document
        items['category'] = category                  # 9- news section if any
        items['images'] = image_dict                  # 10- dictionary of images
        items['reactions'] = reactions                # 11- number of reactions
        items['created_at'] = created_at              # 12- date and time of scraping
        items['sitemap_url'] = sitemap_url            # 13- url of feed if any
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


