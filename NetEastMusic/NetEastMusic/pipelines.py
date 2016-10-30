# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .items import *

import lmdb
import json


class AudioPileline(object):
    def __init__(self):
        lmdb_file = 'lmdb_data'
        self.lmdb_env = lmdb.open(lmdb_file)
        self.cursor = self.lmdb_env.begin(write=True)

    def __del__(self):
        self.lmdb_env.close()

    def process_item(self, item, spider):
        if isinstance(item, SongItem):
            j = {'album_name': item['album_name'], 'song_name': item['song_name']}
            s = json.dumps(j)
            self.cursor.put(s, item['audio'])
            self.cursor.commit()
        return item
