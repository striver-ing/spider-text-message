# encoding=utf8
import sys
sys.path.append("..")

import threading
import fileinput
import base.constance as Constance
import utils.tools as tools
from utils.log import log

db = tools.getConnectedDB()

class AddRootUrl(threading.Thread):
    _addUrlFuncs = []

    def __init__(self):
        super(AddRootUrl, self).__init__()

    def run(self):
        website = tools.getConfValue("collector", "website")
        self.registUrlFunc()

        # 执行add url func
        for addUrlFunc in AddRootUrl._addUrlFuncs:
            addWebUrl = addUrlFunc[0]
            domain = addUrlFunc[1]

            if website == 'all':
                addWebUrl()
            elif website == domain:
                addWebUrl()

    def addUrl(self, url, websiteId, description = '', depth = 0, status = Constance.TODO):
        try:
            urlDict = {'url':url, 'description':description, 'website_id':websiteId, 'depth':depth, 'status':Constance.TODO}
            db.urls.save(urlDict)
        except Exception as e:
            pass

    # 注册添加url的方法
    def registUrlFunc(self):
        AddRootUrl._addUrlFuncs.append([self.addIFengUrl, Constance.IFENG])
        AddRootUrl._addUrlFuncs.append([self.addSoHuUrl, Constance.SOHU])
        AddRootUrl._addUrlFuncs.append([self.addTencentUrl, Constance.TENCENT])
        AddRootUrl._addUrlFuncs.append([self.addSinaUrl, Constance.SINA])
        AddRootUrl._addUrlFuncs.append([self.addCCTVUrl, Constance.CCTV])
        AddRootUrl._addUrlFuncs.append([self.addPeopleUrl, Constance.PEOPLE])
        AddRootUrl._addUrlFuncs.append([self.addWangYiUrl, Constance.WANG_YI])
        AddRootUrl._addUrlFuncs.append([self.addXinHuaUrl, Constance.XIN_HUA])

    # 添加凤凰url
    def addIFengUrl(self):
        baseUrl = "http://www.ifeng.com/"
        websiteId = tools.getWebsiteId(Constance.IFENG)
        self.addUrl(baseUrl, websiteId)

    def addSoHuUrl(self):
        baseUrl = "http://www.sohu.com/"
        websiteId = tools.getWebsiteId(Constance.SOHU)
        self.addUrl(baseUrl, websiteId)

    # 添加腾讯url
    def addTencentUrl(self):
        baseUrl = "http://www.qq.com"
        websiteId = tools.getWebsiteId(Constance.TENCENT)
        self.addUrl(baseUrl, websiteId)

    # 添加新浪url
    def addSinaUrl(self):
        baseUrl = "http://www.sina.com.cn/"
        websiteId = tools.getWebsiteId(Constance.SINA)
        self.addUrl(baseUrl, websiteId)

    def addCCTVUrl(self):
        baseUrl = "http://www.cctv.com/"
        websiteId = tools.getWebsiteId(Constance.CCTV)
        self.addUrl(baseUrl, websiteId)

    def addPeopleUrl(self):
        baseUrl = "http://www.people.com.cn/"
        websiteId = tools.getWebsiteId(Constance.PEOPLE)
        self.addUrl(baseUrl, websiteId)

    def addWangYiUrl(self):
        baseUrl = "http://www.163.com/"
        websiteId = tools.getWebsiteId(Constance.WANG_YI)
        self.addUrl(baseUrl, websiteId)

    def addXinHuaUrl(self):
        baseUrl = "http://www.xinhuanet.com/"
        websiteId = tools.getWebsiteId(Constance.XIN_HUA)
        self.addUrl(baseUrl, websiteId)