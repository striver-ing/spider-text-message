# encoding=utf-8
import sys
sys.path.append("..\..")
#sys.setdefaultencoding('utf-8')

import re
import requests
import fileinput
import utils.tools as tools
import html_parser.base_paser as basePaser
from html_parser.base_paser import *
from requests import exceptions
from requests import Request, Session

def parseUrl(urlInfo):
    log.debug('处理 %s'%urlInfo)

    url = urlInfo['url']
    depth = urlInfo['depth']
    websiteId = urlInfo['website_id']
    description = urlInfo['description']


    try:
        # response = requests.get(url, timeout=5)
        # response.encoding='utf-8'

        html = tools.getHtml(url)
        if html == None:
            basePaser.updateUrl(sourceUrl, Constance.TODO)
            return
    except exceptions.Timeout as e:
        log.error(e.message)
        basePaser.updateUrl(url, Constance.DONE)
    else:
        # if response.status_code < 300:
        log.debug("解析页面开始...")
        #html = response.text
        urls = tools.getInfo(html, 'href="(.+?)"')
        urls = tools.filterDomain(urls, 'sina.com.cn')

        # # 过滤部分视频
        # lineList = []
        # for line in fileinput.input('../filterRule.txt'):
        #     lineList.append(line.strip())

        # urls = tools.filterRule(urls, lineList)
        # 过滤非http开头的url
        urls = tools.filterHttp(urls)
        # 获取url信息开始
        log.debug("url=%s"%url)

        # 获取title
        reg = '<h1.*?>(.*?)</h1>'
        title = ''.join(tools.getInfo(html, reg))
        log.debug("取到标题：%s"%title)

        # 获取正文区域
        reg = 'id="articleContent">(.+?)<p class="article-editor"'
        content = ''.join(tools.getInfo(html, reg))

        # 获取正文
        regex = ['<div.+?>','<!--.+?-->','<ins.+?</ins>', '<script.+?</script>','<img.+>','<strong>|</strong>', '<span.+?</span>','<p>|</p>','&nbsp;']

        for reg in regex:
            content = tools.replaceStr(content, reg)

        content = content.strip()
        log.debug("取到正文：%s"%content)

            # # 获取编码
            # reg = '<meta charset="(.*?)">'
            # charset = ''.join(tools.getInfo(html, reg))
            # log.debug("取到编码：%s"%charset)

            # # 获取发布时间
            # reg = '"a_time">(.*?)</'
            # releaseTime = ''.join(tools.getInfo(html, reg))
            # log.debug("取到发布时间：%s"%releaseTime)

            # # 获取作者
            # reg = '责任编辑：(.*?)</'
            # author = ''.join(tools.getInfo(html, reg))
            # log.debug("取到作者：%s"%author)

            # # 获取keyword
            # reg = '<meta name="keywords" content="(.*?)">'
            # keyword = ''.join(tools.getInfo(html, reg))
            # log.debug("取到关键字：%s"%keyword)

            # 存数据库
        if (title != '' and content != ''):
            basePaser.addTextInfo(websiteId, url, title, content)#, author, releaseTime, charset, keyword)

        for url in urls:
            log.debug("保存url到DB: %s"%url)
            basePaser.addUrl(url, websiteId, depth + 1, '')

        basePaser.updateUrl(url, Constance.DONE)

# url = 'http://finance.sina.com.cn/china/gncj/2016-11-23/doc-ifxxwrwk1733242.shtml'
# # s = Session()
# # headers = {"Content-Type":"zh"}
# # req = Request('GET', url, headers = headers)
# # prepped = req.prepare()
# # resp = s.send(prepped, timeout=5)

# # response = requests.get('http://finance.sina.com.cn/china/gncj/2016-11-23/doc-ifxxwrwk1733242.shtml', timeout=5)
# # log.debug("解析页面开始...")
# # response.encoding='utf-8'
# # resp.encoding='utf-8'
# html = tools.getHtml(url)


# # 获取title
# reg = '<h1.*?>(.*?)</h1>'
# title = ''.join(tools.getInfo(html, reg))
# log.debug("取到标题：%s"%title)

# reg = 'id="articleContent">(.+?)<p class="article-editor"'
# content = ''.join(tools.getInfo(html, reg))
# # regex = ['<div.+?>','<!--.+?-->','<ins.+?</ins>', '<script.+?</script>','<img.+>','<strong>|</strong>', '<span.+?</span>','<p>|</p>']

# # for reg in regex:
# #     content = tools.replaceStr(content, reg)

# content = content.strip()
# print(html)