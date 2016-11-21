# encoding=utf8
from urllib import request
import re
import pymongo
import json
import configparser #读配置文件的
from urllib.parse import quote
import sys
sys.path.append("..")
from utils.log import log

def getHtml(url, code = 'utf-8'):
    html = None
    try:
        page = request.urlopen(quote(url,safe='/:?=&'), timeout = 3)
        html = page.read().decode(code,'ignore')
        page.close()

    except Exception as e:
        log.error(e)
    return html

def getUrls(html):
    urls = re.compile('<a.*?href="(https?.*?)"').findall(str(html))
    return list(set(urls))

def fitUrl(urls, key):
    fitUrls = []
    for link in urls:
        if key in link:
            fitUrls.append(link)
    return list(set(fitUrls))

def getInfo(html,regexs, allowRepeat = False):
    regexs = isinstance(regexs, str) and [regexs] or regexs

    for regex in regexs:
        infos = re.findall(regex,str(html),re.S)
        # infos = re.compile(regexs).findall(str(html))
        if len(infos) > 0:
            break

    return allowRepeat and infos or list(set(infos))

##################################################
"""
    匹配相关函数
"""
# 匹配域名
def filterDomain(urls, domain):
    '''
    @summary:  通过域名过滤不是matchStr所在的URL
    ---------
    @param urls: URL 列表
    @param domain: 所需域名
    ---------
    @result: 返回一个过滤后新的列表
    '''
    log.debug("解析域名....")
    urls = isinstance(urls, str) and [urls] or urls
    newUrls = []
    for url in urls:
        try:
            if get_tld(url) == domain:
                newUrls.append(url)
        except Exception as e:
            log.debug("Unknow")

    return newUrls

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
    log.debug("过滤匹配...")
    urls = isinstance(urls, str) and [urls] or urls
    rules = isinstance(rules, str) and [rules] or rules

    newUrls = []
    for url in urls:
        for rule in rules:
            if url.find(rule) == -1:
                newUrls.append(url)
                break

    return newUrls
##################################################

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