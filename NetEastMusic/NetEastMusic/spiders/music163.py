# -*- coding: utf-8 -*-
from __future__ import absolute_import
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import FormRequest, Request
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
import json

from ..components import get_comments
from ..components import get_data_for_post
from ..items import *

# globals
data = get_data_for_post()
headers = {
    'Cookie': 'appver=1.5.0.75771;',
    'Referer': 'http://music.163.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.8 Safari/537.36'
}
api_user_playlist = 'http://music.163.com/api/user/playlist?'

class Music163Spider(CrawlSpider):
    name = "music163"
    allowed_domains = ["music.163.com"]
    start_urls = ["http://music.163.com/discover/artist"]
    rules = [Rule(LinkExtractor(allow='/artist\?id=\d+')),
             Rule(LinkExtractor(allow='/discover/artist/cat\?id=\d+')),
             # Rule(LinkExtractor(allow=(r'/discover/artist/cat\?id=\d+&initial=\d+'))),
             Rule(LinkExtractor(allow='/song\?id=\d+'), callback="parse_song")]

    # get songs comments
    def parse_song(self, response):
        url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + response.url[29:]+'/?csrf_token='
        f = FormRequest(url, formdata=data, headers=headers, callback=self.parse_user_id)
        yield f

    # generate user ids
    def parse_user_id(self, response):
        result = json.loads(response.text)
        comments = result['comments']
        hotComments = result['hotComments']

        for comment in comments:
            userId = comment['user']['userId']
            req = {"offset": 0, "limit": 100, "uid": userId}
            url = api_user_playlist + urlencode(req)
            meta = {'req':req, 'name':comment['user']['nickname']}
            yield Request(url=url, callback=self.parse_user_playlist, meta=meta)

        for comment in hotComments:
            userId = comment['user']['userId']
            req = {"offset": 0, "limit": 100, "uid": userId}
            url = api_user_playlist + urlencode(req)
            meta = {'req': req, 'name':comment['user']['nickname']}
            yield Request(url=url, callback=self.parse_user_playlist, meta=meta)

    # sample
    # http://music.163.com/api/user/playlist?uid=107273856&limit=100&offset=0
    def parse_user_playlist(self, response):
        json_object = json.loads(response.text)

        # 判断是否为第一次
        if response.meta.has_key('item'):
            item = response.meta['item']
        else:
            item = UserItem()
            item['name'] = response.meta['name']
            item['uid'] = response.meta['req']['uid']
            item['playlists'] = []

        for playlist in json_object['playlist']:
            item['playlists'].append(playlist['id'])

        if json_object['more']:
            req = response.meta['req']
            req['offset'] = int(req['offset']) + 100
            url = api_user_playlist + urlencode(req)
            yield Request(url=url, callback=self.parse_user_playlist, meta={'req':req, 'item':item})
        else:
            yield item
