# encoding=utf8
import sys
sys.path.append("../..")

import html_parser.base_paser as basePaser
from html_parser.base_paser import *

DEBUG = False

# not use url
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

#外部传进url
def parseUrl(urlInfo):
    log.debug('处理 %s'%urlInfo)

    sourceUrl = urlInfo['url']
    depth = urlInfo['depth']
    websiteId = urlInfo['website_id']
    description = urlInfo['description']

    # 使用urlopen网页有时乱码 用get请求 然后设置编码解决了问题
    html = tools.getHtmlByGet(sourceUrl, '')

    if not DEBUG:
        if html == None:
            if sourceUrl == Constance.TENCENT:
                basePaser.updateUrl(sourceUrl, Constance.TODO)
            else:
                basePaser.updateUrl(sourceUrl, Constance.EXCEPTION)
            return

        regex = '[\u4e00-\u9fa5]+'
        chineseWord = tools.getInfo(html, regex)
        if not chineseWord:
            basePaser.updateUrl(sourceUrl, Constance.DONE)
            return

        # 取当前页面的全部url
        urls = tools.getUrls(html)

        # 过滤掉外链接 添加到数据库
        fitUrl = tools.fitUrl(urls, "qq.com")
        fitUrl = tools.filterRule(fitUrl, lineList)
        for url in fitUrl:
            # log.debug('url = ' + url)
            basePaser.addUrl(url, websiteId, depth + 1)


    # 取当前页的文章信息
    # 标题
    regexs = '<h1.*?>(.*?)</h1>'
    title = tools.getInfo(html, regexs)
    title = title and title[0] or ''
    title = tools.delHtmlTag(title)
    # 内容
    regexs = ['bossZone="content">(.+?)正文已结束.+?</span>',
              'id="articleContent">(.*?)<div class="hasc">'
             ]

    content = tools.getInfo(html, regexs)
    content = content and content[0] or ''
    content = tools.delHtmlTag(content)

    log.debug('''
                depth     = %d
                sourceUrl = %s
                title     = %s
                content   =  %s
             '''%(depth, sourceUrl, title, content))

    if not DEBUG:
        if content and title:
            basePaser.addTextInfo(websiteId, sourceUrl, title, content)

        # 更新sourceUrl为done
        basePaser.updateUrl(sourceUrl, Constance.DONE)

if __name__ == '__main__':
    print('main')
    DEBUG = True
    url = 'http://news.qq.com/a/20161127/005993.htm'
    haha = {'url': url, 'website_id': '582ea577350b654b67dc8ac8', 'depth': 1, 'description': ''}
    parseUrl(haha)