# encoding=utf8

import sys
sys.path.append("..")

import re
import pymongo
import json
import configparser #读配置文件的
from urllib.parse import quote
from utils.log import log
from tld import get_tld
from urllib import request
# from selenium import webdriver
import requests
import time
from threading import Timer
import functools
import datetime
import socket
socket.setdefaulttimeout(3.0)

TIME_OUT = 30
TIMER_TIME = 5

def getHtml(url, code = 'utf-8'):
    html = None
    if not url.endswith('.exe') and not url.endswith('.EXE'):
        page = None
        try:
            def timeout_handler(response):
                response.close()

            page = request.urlopen(quote(url,safe='/:?=&'), timeout = TIME_OUT)
            # 设置定时器 防止在read时卡死
            t = Timer(TIMER_TIME, timeout_handler, [page])
            t.start()
            html = page.read().decode(code,'ignore')
            t.cancel()

        except Exception as e:
            log.error(e)
        finally:
            page and page.close()
    return html if len(html) < 1024 * 1024 else None  # 不是网页的不要

# def getHtmlByWebDirver(url):
#     html = None
#     try:
#         driver = webdriver.PhantomJS(executable_path = 'D:/software/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs')
#         driver.get(url)
#         # time.sleep(10)
#         html = driver.page_source
#         driver.close()
#     except Exception as e:
#         log.error(e)
#     return html

def getHtmlByGet(url, code = 'utf-8'):
    html = None
    if not url.endswith('.exe') and not url.endswith('.EXE'):
        r = None
        try:
            r = requests.get(url, timeout = TIME_OUT)
            if code:
                r.encoding = code
            html = r.text

        except Exception as e:
            log.error(e)
        finally:
            r and r.close()
    return html if len(html) < 1024 * 1024 else None

def getUrls(html):
    urls = re.compile('<a.*?href="(https?.*?)"').findall(str(html))
    return list(set(urls))

def fitUrl(urls, identis):
    identis = isinstance(identis, str) and [identis] or identis
    fitUrls = []
    for link in urls:
        for identi in identis:
            if identi in link:
                fitUrls.append(link)
    return list(set(fitUrls))

def getInfo(html,regexs, allowRepeat = False):
    regexs = isinstance(regexs, str) and [regexs] or regexs

    for regex in regexs:
        infos = re.findall(regex,str(html),re.S) #不是网页可能会卡死 比如apk
        # infos = re.compile(regexs).findall(str(html))
        if len(infos) > 0:
            break

    return allowRepeat and infos or list(set(infos))

def delHtmlTag(content):
    content = replaceStr(content, '<script(.|\n)*?</script>')
    content = replaceStr(content, '<style(.|\n)*?</style>')
    content = replaceStr(content, '<!--(.|\n)*?-->')
    content = replaceStr(content, '<(.|\n)*?>')
    content = replaceStr(content, '&.*?;')
    content = replaceStr(content, '\s')

    return content

def isHaveChinese(content):
    regex = '[\u4e00-\u9fa5]+'
    chineseWord = getInfo(content, regex)
    return chineseWord and True or False

##################################################
"""
    匹配相关函数
"""
# 匹配域名
def filterDomain(urls, domain):
    '''
    @summary:  通过域名过滤不是domain所在的URL
    ---------
    @param urls: URL 列表
    @param domain: 所需域名
    ---------
    @result: 返回一个过滤后新的列表
    '''
    urls = isinstance(urls, str) and [urls] or urls

    def _Rule(url):
        try:
            return get_tld(url) == domain
        except Exception as e:
            log.debug("******** Invalid URL %s ********"%url)
            return False

    return filter(_Rule, urls)

# 规则匹配
def filterRule(urls, rules):
    '''
    @summary: 通过ruleList过滤不符合规则的URL
    ---------
    @param urls: URL 列表
    @param rules: 需要过滤的关键字字符串或列表
    ---------
    @result: 返回一个过滤后新的列表
    '''
    urls = isinstance(urls, str) and [urls] or urls
    rules = isinstance(rules, str) and [rules] or rules

    def _Rule(url):
        for rule in rules:
            if url.find(rule) != -1:
                return False
        return True

    return filter(_Rule, urls)

def filterHttp(urls, rule  = 'http'):
    '''
    @summary: 过滤不是http开头的url
    ---------
    @param urls: url list
    @param rule: must be str  only one
    ---------
    @result: filtered list
    '''
    urls = isinstance(urls, str) and [urls] or urls
    def _Rule(url):
        if re.match(rule, url):
            return True
        return False
    return filter(_Rule, urls)

##################################################
def getJson(jsonStr):
    '''
    @summary: 取json对象
    ---------
    @param jsonStr: json格式的字符串
    ---------
    @result: 返回json对象
    '''

    return json.loads(jsonStr)


##################################################
def replaceStr(sourceStr, regex, replaceStr = ''):
    '''
    @summary: 替换字符串
    ---------
    @param sourceStr: 原字符串
    @param regex: 正则
    @param replaceStr: 用什么来替换 默认为''
    ---------
    @result: 返回替换后的字符串
    '''
    strInfo = re.compile(regex)
    return strInfo.sub(replaceStr, sourceStr)

##################################################
def getConfValue(section, key):
    cf = configparser.ConfigParser()
    cf.read("../spider.conf")
    return cf.get(section, key)

#################时间转换相关####################
def timeListToString(timeList):
    times = 0
    for word in timeList:
        times = times + timeToString(word)
    return str(times)

def timeToString(time):
    timeList = time.split(':')
    if len(timeList) == 3 :
        return int(timeList[0]) * 3600 + int(timeList[1]) * 60 + int(timeList[2])
    elif len(timeList) == 2:
        return int(timeList[0]) * 60 + int(timeList[1])
    else: return 0

##################################################
class DB():
    client = pymongo.MongoClient("localhost",27017)
    db = client.spider_text_message

db = DB.db
def getConnectedDB():
    return db

def dbSave(collection,dictInfo):
    db.getCollection(collection).save(dictInfo)

def dbUpdata(collection,dictInfo,newdictInfo):
    db.getCollection(collection).update(dictInfo,{'$set':newdictInfo})

def dbFind(collection,condition):
    return db.getCollection(collection).find(condition)


##################################################
def getWebsiteId(domain):
    website = list(db.website.find({'domain':domain}))
    websiteId = None
    if len(website) > 0:
        websiteId = website[0]['_id']
    else:
        log.warning('website表中无%s信息，需先手动添加'%domain)

    return websiteId

################################################

def log_function_time(func):
    try:
        @functools.wraps(func)  #将函数的原来属性付给新函数
        def calculate_time(*args, **kw):
            began_time = time.time()
            func(*args, **kw)
            end_time = time.time()
            log.info(func.__name__ + " run time  = " + str(end_time - began_time))
        return calculate_time
    except:
        log.info('求取时间无效 因为函数参数不符')
        return func
