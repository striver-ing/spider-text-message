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

    html = tools.getHtml(sourceUrl, 'gb2312')
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.EXCEPTION)
        return

    # 取当前页面的全部url
    urls = tools.getUrls(html)

    # 过滤掉外链接 添加到数据库
    fitUrl = tools.fitUrl(urls, "sohu.com")
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
    regexs = ['<div class="content clear clearfix".*?>(.*?)</div>',
              '<div class="box_con".*?>(.*?)<div class="edit clearfix"',
              '<div class="show_text">(.*?)</div>',
              '<div class="text">.*?<hr class="nonehr">',
              '<div itemprop="articleBody">(.*?)<div style="display:none;">',
              '<article>(.*?)</article>']

    content = tools.getInfo(html, regexs)
    content = content and content[0] or ''
    content = tools.delHtmlTag(content)

    log.debug('''
                sourceUrl = %s
                title     = %s
                content   =  %s
             '''%(sourceUrl, title, content))

    if content:
        basePaser.addTextInfo(websiteId, sourceUrl, title, content)

    # 更新sourceUrl为done
    basePaser.updateUrl(sourceUrl, Constance.DONE)

# url = 'http://yule.sohu.com/20161122/n473807549.shtml'
# haha = {'url': url, 'website_id': '582ea577350b654b67dc8ac8', 'depth': 1, 'description': ''}
# parseUrl(haha)


