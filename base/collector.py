# -*- coding: utf-8 -*-
'''
Created on 2016-12-23 11:24
---------
@summary: url 管理器 负责取url 存储在环形的urls列表中
---------
@author: Boris
'''

import sys
sys.path.append("..")

import threading
import time
import base.constance as Constance
import utils.tools as tools
from utils.log import log
import utils.export_data as exportData
import os
import time

mylock = threading.RLock()

#test
DEBUG =False
DEPTH = 0

class Singleton(object):
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst=super(Singleton,cls).__new__(cls,*args,**kwargs)

        return cls._inst

class Collector(threading.Thread, Singleton):
    _db = tools.getConnectedDB()
    _threadStop = False
    _urls = []
    _nullTimes = 0
    _readPos = -1
    _writePos = -1
    _maxSize = int(tools.getConfValue("collector", "max_size"))
    _interval = int(tools.getConfValue("collector", "sleep_time"))
    _allowedNullTimes = int(tools.getConfValue("collector", 'allowed_null_times'))
    _website = tools.getConfValue("collector", "website")
    _depth = int(tools.getConfValue("collector", "depth"))
    _urlCount = int(tools.getConfValue("collector", "url_count"))

    #初始时将正在做的任务至为未做
    beginTime = time.time()
    # _db.urls.update({'status':Constance.DOING}, {'$set':{'status':Constance.TODO}}, multi=True)
    endTime = time.time()
    log.debug('update url time' + str(endTime - beginTime) )

    if DEBUG:
        log.debug("is debug depth = %s"%DEPTH)

    def __init__(self):
        super(Collector, self).__init__()

    def run(self):
        while not Collector._threadStop:
            self.__inputData()
            time.sleep(Collector._interval)

    def stop(self):
        Collector._threadStop = True

    @tools.log_function_time
    def __inputData(self):
        log.debug('buffer size %d'%self.getMaxReadSize())
        log.debug('buffer can write size = %d'%self.getMaxWriteSize())
        if self.getMaxWriteSize() == 0:
            log.debug("collector 已满 size = %d"%self.getMaxReadSize())
            return

        beginTime = time.time()

        urlCount = Collector._urlCount if Collector._urlCount <= self.getMaxWriteSize() else self.getMaxWriteSize()

        if DEBUG:
            urlsList = Collector._db.urls.find({"status":Constance.TODO, "depth":DEPTH},{"url":1, "_id":0,"depth":1, "description":1, "website_id":1}).sort([("depth",1)]).limit(urlCount)
        elif Collector._website == 'all':
            urlsList = Collector._db.urls.find({"status":Constance.TODO, "depth":{"$lte":Collector._depth}},{"url":1, "_id":0,"depth":1, "description":1, "website_id":1}).sort([("depth",1)]).limit(urlCount)#sort -1 降序 1 升序
        else:
            websiteId = tools.getWebsiteId(Collector._website)
            urlsList = Collector._db.urls.find({"status":Constance.TODO, "website_id":websiteId, "depth":{"$lte":Collector._depth}},{"url":1, "_id":0,"depth":1, "description":1, "website_id":1}).sort([("depth",1)]).limit(urlCount)

        endTime = time.time()

        urlsList = list(urlsList)

        log.debug('get url time ' + str(endTime - beginTime) + " size " + str(len(urlsList) ))

        # 存url
        self.putUrls(urlsList)

        #更新已取到的url状态为doing
        beginTime = time.time()
        for url in urlsList:
            Collector._db.urls.update(url, {'$set':{'status':Constance.DOING}})
        endTime = time.time()
        log.debug('update url time ' + str(endTime - beginTime) )

        if self.isAllHaveDone():
            self.stop()
            exportData.export()

    def isFinished(self):
        return Collector._threadStop

    def isAllHaveDone(self):
        if Collector._urls == []:
            Collector._nullTimes += 1
            if Collector._nullTimes >= Collector._allowedNullTimes:
                return True
        else:
            Collector._nullTimes = 0
            return False

    def getMaxWriteSize(self):
        size = 0
        if Collector._readPos == Collector._writePos:
            size = Collector._maxSize
        elif Collector._readPos < Collector._writePos:
            size = Collector._maxSize - (Collector._writePos - Collector._readPos)
        else:
            size = Collector._readPos - Collector._writePos

        return size

    def getMaxReadSize(self):
        return Collector._maxSize - self.getMaxWriteSize()

    def putUrls(self, urlsList):
        # 添加url 到 _urls
        urlCount = len((urlsList))
        endPos = urlCount + Collector._writePos + 1
        # 判断是否超出队列容量 超出的话超出的部分需要从头写
        # 超出部分
        overflowEndPos = endPos - Collector._maxSize
        # 没超出部分
        inPos =  endPos if endPos <= Collector._maxSize else Collector._maxSize

        # 没超出部分的数量
        urlsListCutPos = inPos - Collector._writePos - 1

        beginTime = time.time()
        mylock.acquire() #加锁

        Collector._urls[Collector._writePos + 1 : inPos] = urlsList[:urlsListCutPos]
        if overflowEndPos > 0:
            Collector._urls[:overflowEndPos] = urlsList[urlsListCutPos:]

        mylock.release()
        log.debug('put url time ' + str( time.time() - beginTime)  + " size " +  str(len(urlsList)) )

        Collector._writePos += urlCount
        Collector._writePos %= Collector._maxSize




    @tools.log_function_time
    def getUrls(self, count):
        mylock.acquire() #加锁
        urls = []

        count = count if count <= self.getMaxReadSize() else self.getMaxReadSize()
        endPos = Collector._readPos + count + 1
        if endPos > Collector._maxSize:
            urls.extend(Collector._urls[Collector._readPos + 1:])
            urls.extend(Collector._urls[: endPos % Collector._maxSize])
        else:
            urls.extend(Collector._urls[Collector._readPos + 1: endPos])

        Collector._readPos += len(urls)
        Collector._readPos %= Collector._maxSize

        mylock.release()

        return urls
