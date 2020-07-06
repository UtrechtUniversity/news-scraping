# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# import sqlite3
import mysql.connector


class NewsScrapePipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        # self.conn =sqlite3.connect("scraped_news.db")
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='mydb01',
            database='news'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""Drop TABLE IF EXISTS news_tb""")
        self.curr.execute("""create table news_tb(
                            article_id text,
                            title text,
                            article_info text,
                            article_body text,
                            publication_date text,
                            publication_time text,
                            created_at datetime,
                            image text,
                            reactions text,
                            author text,
                            doctype text,
                            url text,
                            tags text,
                            twitter text,
                            facebook text,
                            iframe text
                            )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        # self.curr.execute("""insert into news_tb values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
        self.curr.execute("""insert into news_tb values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )""",
                          (
                              item['article_id'],
                              item['title'],
                              item['article_info'],
                              item['article_body'],
                              item['publication_date'],
                              item['publication_time'],
                              item['created_at'],
                              item['image'],
                              item['reactions'],
                              item['author'],
                              item['doctype'],
                              item['url'],
                              item['tags'],
                              item['twitter'],
                              item['facebook'],
                              item['iframe']

                          ))
        self.conn.commit()
