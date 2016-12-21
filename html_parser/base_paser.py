# encoding=utf8
import sys
sys.path.append("..")

import base.constance as Constance
import utils.tools as tools
from utils.log import log

db = tools.getConnectedDB()

def getWebsiteId(domain):
    website = list(db.website.find({'domain':domain}))
    websiteId = None
    if len(website) > 0:
        websiteId = website[0]['_id']
    else:
        log.warning('website表中无%s信息，需先手动添加'%domain)

    return websiteId

def getRegexTypeId(regType):
    regexType = list(db.regex_type.find({'type':regType}))
    regexTypeId = None
    if len(regexType) > 0:
        regexTypeId = regexType[0]['_id']
    else:
        log.warning('regex_type无%s信息，需先手动添加'%regType)

    return regexTypeId

def getRegex(websiteId, regTypeId):
    regexs = []
    for regex in db.regexs.find({'website_id':websiteId, 'type_id':regTypeId}, {'regex':1, '_id':0}):
        regexs.append(regex['regex'])
    return regexs

##################################################
# @tools.log_function_time
def addUrl(url, websiteId, depth, description = '', status = Constance.TODO):
    try:
        urlDict = {'url':url, 'website_id':websiteId, 'depth':depth, 'description':description, 'status':status}
        db.urls.save(urlDict)
    except Exception as e:
        # log.debug('已存在 url ' + url)
        pass

@tools.log_function_time
def updateUrl(url, status):
    db.urls.update({'url':url}, {'$set':{'status':status}}, multi=True)
    log.debug('update url status = %d url = %s'%(status, url))

@tools.log_function_time
def addTextInfo(websiteId, url, title, content, author = '', releaseTime = '', charset = '', keyword = ''):
    '''
    @summary: 添加文章信息
    ---------
    @param websiteId:网站id
    @param url:文章url
    @param title:文章标题
    @param content:文章内容
    @param author:文章作者
    @param releaseTime:文章发布时间
    @param charset: 编码
    @param keyword: 网页中<keyword>关键字
    ---------
    @result:
    '''

    textInfoDict = {
        'website_id':websiteId,
        'url':url,
        'title':title,
        'content':content,
        'author':author,
        'release_time':releaseTime,
        'charset':charset,
        'keyword':keyword,
        'read_status':0
        }

    # # 查找数据库，根据url和websiteid看是否有相同的纪录，若有，则比较纪录信息，将信息更全的纪录更新到数据库中
    # for doc in db.text_info.find({'website_id':websiteId, 'url':url}, {'_id':0}):
    #     isDiffent = False
    #     warning = '\n' + '-' * 50 + '\n'
    #     for key, value in doc.items():
    #         if len(str(doc[key])) < len(str(textInfoDict[key])):
    #             isDiffent = True
    #             warning = warning + '更新 old %s: %s\n     new %s: %s\n'%(key, doc[key], key, textInfoDict[key])
    #             doc[key] = textInfoDict[key]

    #         else:
    #             warning = warning + '留守 old %s: %s\n     new %s: %s\n'%(key, doc[key], key, textInfoDict[key])

    #     if isDiffent:
    #         warning = '已存在：\n' + warning + '-' * 50
    #         log.warning(warning)

    #         db.text_info.update({'website_id':websiteId, 'url':url}, {'$set':doc})
    #     else:
    #         log.warning('已存在url:  ' + url)
    #     return

    try:
        db.text_info.save(textInfoDict)
    except Exception as e:
        log.debug('已存在 textInfoDict ' + str(textInfoDict))