# encoding=utf8
import sys
sys.path.append("../..")

import html_parser.base_paser as basePaser
from html_parser.base_paser import *

#外部传进url
def parseUrl(urlInfo):
    log.debug('处理 %s'%urlInfo)

    url = urlInfo['url']
    depth = urlInfo['depth']
    websiteId = urlInfo['website_id']
    description = urlInfo['description']

    html = tools.getHtml(url)
    if html == None:
        basePaser.updateUrl(sourceUrl, Constance.TODO)
        return
