# -*- coding: utf-8 -*-
'''
Created on 2016-10-26 13:52
---------
@summary: 清空urls表
---------
@author: Boris
'''

import pymongo

client = pymongo.MongoClient("localhost",27017)
db = client.spider_text_message

db.urls.remove()