# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    uid = scrapy.Field()
    playlists = scrapy.Field()

class SongItem(scrapy.Item):
    comments = scrapy.Field()
    song_url = scrapy.Field()
    name = scrapy.Field()
