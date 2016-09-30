# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    name = scrapy.Field()
    uid = scrapy.Field()
    playlists = scrapy.Field()

class PlaylistItem(scrapy.Item):
    name = scrapy.Field()
    uid = scrapy.Field()
    songs = scrapy.Field()

class SongItem(scrapy.Item):
    uid = scrapy.Field()
    name = scrapy.Field()
    mp3Url = scrapy.Field()
