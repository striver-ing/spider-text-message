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

def parseUrl(urlInfo):
    log.debug('处理 %s'%urlInfo)

    url = urlInfo['url']
    depth = urlInfo['depth']
    websiteId = urlInfo['website_id']
    description = urlInfo['description']

    try:
        response = requests.get(url, timeout=5)
    except Exception as e:
        log.error(e)
        basePaser.updateUrl(url, Constance.DONE)
    else:
        if response.status_code < 300:
            log.debug("解析页面开始...")
            html = response.text
            urls = tools.getInfo(html, 'href="(.+?)"')
            urls = tools.filterDomain(urls, 'qq.com')

            # 过滤部分视频
            urls = tools.filterRule(urls, lineList)
            urls = tools.filterHttp(urls)
            # 获取url信息开始
            log.debug("url=%s"%url)

            # 获取title
            reg = '<title>(.*?)</title>'
            title = ''.join(tools.getInfo(html, reg))
            log.debug("取到标题：%s"%title)

            # 获取正文区域
            reg = 'bossZone="content">(.+?)正文已结束.+?</span>'
            mainArticle = tools.getInfo(html, reg);

            # 获取正文
            reg = '<P.*?>(.*?)</P>'
            content = ''.join(re.findall(reg,str(mainArticle),re.S))

            regex = ['<script.+</script>','<style.+</style>','<div.+</div>','<!--.*?-->','\\|\\\\|r|n','\\\\','u3000','<.+?>']
            for reg in regex:
                content = tools.replaceStr(content, reg)
            content = content.strip()
            log.debug("取到正文：%s"%content)

            # 获取编码
            reg = '<meta charset="(.*?)">'
            charset = ''.join(tools.getInfo(html, reg))
            log.debug("取到编码：%s"%charset)

            # 获取发布时间
            reg = '"a_time">(.*?)</'
            releaseTime = ''.join(tools.getInfo(html, reg))
            log.debug("取到发布时间：%s"%releaseTime)

            # 获取作者
            reg = '责任编辑：(.*?)</'
            author = ''.join(tools.getInfo(html, reg))
            log.debug("取到作者：%s"%author)

            # 获取keyword
            reg = '<meta name="keywords" content="(.*?)">'
            keyword = ''.join(tools.getInfo(html, reg))
            log.debug("取到关键字：%s"%keyword)

            # 存数据库
            if (title != '' and content != ''):
                basePaser.addTextInfo(websiteId, url, title, content, author, releaseTime, charset, keyword)

            for url in urls:
                log.debug("保存url到DB: %s"%url)
                basePaser.addUrl(url, websiteId, depth + 1, '')

            basePaser.updateUrl(url, Constance.DONE)
        else:
            basePaser.updateUrl(url, Constance.DONE)


lineList = [
'service.qq.com',
'pvp.qq.com',
'vip.qq.com',
'iwan.qq.com',
'exp.qq.com',
'mil.qq.com',
'qzone.qq.com',
'college.qq.com',
'xw.qq.com',
'open.qq.com',
'stats.2016.qq.com',
'nba.stats.qq.com',
'wj.qq.com',
'browser.qq.com',
'show.qq.com',
'888.qq.com',
'auto.qq.com',
'v.qq.com',
't.qq.com',
'rufodao.qq.com',
'dushu.qq.com',
'ent.qq.com',
'map.qq.com',
'fashion.qq.com',
'kid.qq.com',
'gu.qq.com',
'stockapp.finance.qq.com',
'stockhtm.finance.qq.com',
'stock.qq.com',
'xing.qq.com',
'astro.fashion.qq.com',
'cul.qq.com',
'dajia.qq.com',
'comic.qq.com',
'games.qq.com',
'lol.qq.comic',
'ylzt.qq.com',
'cf.qq.com',
'chuangshi.qq.com',
'tech.qq.com',
'health.qq.com',
'le.qq.com',
'kbs.sports.qq.com',
'sports.qq.com',
'y.qq.com',
'vip.music.qq.com',
'yue.qq.com',
'finance.qq.com',
'digi.tech.qq.com',
'baby.qq.com',
'house.qq.com',
'ru.qq.com',
'dao.qq.com',
'kuaibao.qq.com',
'kb.qq.com',
'class.qq.com',
'ilike.qq.com',
'xf.qq.com',
'gaopeng.qq.com',
'.exe'
]


"""
html =  requests.get('http://sports.qq.com/a/20161122/003622.htm#p=1').text
#urls = tools.filterDomain(urls, 'qq.com')

reg = 'bossZone="content">(.+?)正文已结束.+?</span>'
mainArticle = tools.getInfo(html, reg);
reg = '<P.*?>(.*?)</P>'
content = ''.join(re.findall(reg,str(mainArticle),re.S))
content = tools.replaceStr(content, '<script.+</script>')
content = tools.replaceStr(content, '<style.+</style>')
content = tools.replaceStr(content, '<div.+</div>')
content = tools.replaceStr(content, '<!--.*?-->')
content = tools.replaceStr(content, '\\|\\\\|r|n')
content = tools.replaceStr(content, '\\\\')
content = tools.replaceStr(content, 'u3000')
content = content.strip()
content = tools.replaceStr(content, '<.+?>')
print(content)



url = 'http://www.qq.com'
response = requests.get(url, timeout=5)


urls = []
lineList = []
for line in fileinput.input('../../filterRule.txt'):
urls.append('news.com')
urls.append('http://qq.com')
urls = tools.filterRule(urls, 'qq')

for i in lineList:
    print(i)

for url in urls:
    print(url)
"""