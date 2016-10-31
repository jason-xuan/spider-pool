# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .items import *
from . import settings

import lmdb
import sqlite3
import os
import json

_SQL = {
    'insert': 'INSERT INTO songs (song_name, album_name, audio) '
              'VALUES (?, ?, ?)'
}

class AudioPileline(object):
    def __init__(self):
        is_exist = os.path.isfile(settings.SQLITE)
        self.db = sqlite3.connect(settings.SQLITE)
        self.cur = self.db.cursor()
        # 不存在, 则创建表
        if not is_exist:
            self.cur.execute('''Create Table songs(
            song_name TEXT,
            album_name TEXT,
            audio BLOB,
            PRIMARY KEY (song_name, album_name)
            );
            ''')

    def __del__(self):
        self.cur.close()
        self.db.close()

    def process_item(self, item, spider):
        if isinstance(item, SongAudioItem):
            item['audio'].seek(0)
            audio = item['audio'].read()

            self.cur.execute(_SQL['insert'], (item['song_name'], item['album_name'], audio))
            self.db.commit()
        return item


# class AudioPileline(object):
#     def __init__(self):
#         lmdb_file = 'lmdb_data'
#         self.lmdb_env = lmdb.open(lmdb_file, writemap=True, map_size=int(1e10))
#         self.cursor = self.lmdb_env.begin(write=True)
#
#     def __del__(self):
#         self.lmdb_env.close()
#
#     def process_item(self, item, spider):
#         if isinstance(item, SongAudioItem):
#             j = {'album_name': item['album_name'], 'song_name': item['song_name']}
#             s = json.dumps(j)
#             item['audio'].seek(0)
#             audio = item['audio'].read()
#             self.cursor.put(s, audio)
#             self.cursor.commit()
#         return item
