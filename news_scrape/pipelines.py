
import mysql.connector


class NewsScrapePipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='mydb01',
            database='new_test'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS testnew_tb(
                            id text,
                            title text,
                            teaser text,
                            text text,
                            category text,
                            publication_date text,
                            publication_time text,
                            created_at datetime,
                            images text,
                            reactions text,
                            author text,
                            doctype text,
                            url text,
                            tags text,
                            sitemap_url text
                            )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""insert into testnew_tb values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s
        )""",
                          (
                              item['id'],
                              item['title'],
                              item['teaser'],
                              item['text'],
                              item['category'],
                              item['publication_date'],
                              item['publication_time'],
                              item['created_at'],
                              item['images'],
                              item['reactions'],
                              item['author'],
                              item['doctype'],
                              item['url'],
                              item['tags'],
                              item['sitemap_url']

                          ))
        self.conn.commit()
