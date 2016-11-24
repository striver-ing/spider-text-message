# encoding=utf8
import sys
sys.path.append("../..")

import html_parser.base_paser as basePaser
from html_parser.base_paser import *

#外部传进url
def parseUrl(urlInfo):
    log.debug('处理 %s'%urlInfo)

    sourceUrl = urlInfo['url']
    depth = urlInfo['depth']
    websiteId = urlInfo['website_id']
    description = urlInfo['description']

    html = tools.getHtml(sourceUrl)
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return


    # 取当前页的文章信息
    # 标题
    regexs = '<h1><!--repaste.title.begin-->(.*?)<!--repaste.title.end-->'
    title = tools.getInfo(html, regexs)
    title = title and title[0] or ''
    # 内容
    regexs = ['<!--repaste.body.begin-->(.*?)<!--repaste.body.end-->']

    content = tools.getInfo(html, regexs)
    content = content and content[0] or ''

    content = tools.replaceStr(content, '<script(.|\n)*?</script>')
    content = tools.replaceStr(content, '<(.|\n)*?>')
    content = tools.replaceStr(content, '-->')
    content = tools.replaceStr(content, '&.*?;')
    content = tools.replaceStr(content, '\s')

    log.debug("---------- article ----------\ntitle = %s\ncontent = %s"%(title, content))

    # 判断中英文
    regex = '[\u4e00-\u9fa5]+'
    chineseWord = tools.getInfo(content, regex)

    if chineseWord and content and title:
        basePaser.addTextInfo(websiteId, sourceUrl, title, content)

    # 當前頁是中文， 則把當前頁的子url添加到數據庫
    if chineseWord:
        # 取当前页面的全部url
        urls = tools.getUrls(html)

        # 过滤掉外链接 添加到数据库
        fitUrl = tools.fitUrl(urls, "cctv.com")
        for url in fitUrl:
            # log.debug('url = ' + url)
            basePaser.addUrl(url, websiteId, depth + 1)
    else:
        log.debug('当前页非中文 或 无章信息 %s'%sourceUrl)

    # 更新sourceUrl为done
    basePaser.updateUrl(sourceUrl, Constance.DONE)

# url = 'http://espanol.cctv.com/2016/11/22/ARTI1FKaPF91p4VIp1jerGBx161122.shtml'
# haha = {'url': url, 'website_id': '582ea577350b654b67dc8ac8', 'depth': 1, 'description': ''}
# parseUrl(haha)


