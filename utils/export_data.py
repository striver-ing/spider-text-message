# enconding = utf8
import pymongo
from pymongo.collection import Collection
import urllib.parse
import os
import sys

sys.path.append("..")
from utils.log import log

MONGO_HOST = 'localhost'
MONGO_PORT = 27017

FILE_PATH    = 'D:\\TextMessage\\'
# WEBSITE = "酷六"

class MongoDB():
    def __init__(self, db = '', host = MONGO_HOST, port = MONGO_PORT):
        self.host = host
        self.port = port
        self.db = db

    def getMongoDB(self):
        try:
            self.client = pymongo.MongoClient(self.host, self.port)
            self.db = self.client.spider_text_message  #这需要手动填mongodb数据库名
            return self.db
        except:
            print('connect mongodb error.')

    def close(self):
        self.client.close()

# 二级域名
def getDomain(url):
    proto, rest = urllib.parse.splittype(url)
    res, rest = urllib.parse.splithost(rest)
    rest = res.replace('www.', '')
    return rest

if __name__ == '__main__':
    dataCount = 0

    mongoDB = MongoDB()
    db = mongoDB.getMongoDB()

    if not os.path.exists(FILE_PATH):
        os.removedirs(os.remove(FILE_PATH))

    flag = True
    while flag:
        flag = False
        datas = db.text_info.find({})
        for data in datas:
            url = data['url']
            website = list(db.website.find({'_id':data['website_id']}))[0]['web_name']

            fileName = getDomain(url) + ".txt"
            fileName = FILE_PATH + website + "\\" + fileName

            # 创建文件夹
            if not os.path.exists(FILE_PATH + website + "\\"):
                os.makedirs(FILE_PATH + website + "\\")


            #创建文件 追加方式写入
            file = open(fileName, 'a',  encoding='utf8')

            # 写文件
            print('正在导出 %s 到 %s'%(data['title'], fileName))
            value = (data['title'], data['release_time'], data['charset'], data['author'], data['url'], data['keyword'], data['content'])
            text = \
'''
<text>
<title>%s</title>
<foundtime>%s</foundtime>
<charset>%s</charse>
<author>%s</author>
<Url>%s</Url>
<keyword>%s</keyword>
<summary>%s</summary>
</text>

'''
            file.write(text%value)
            dataCount = dataCount + 1


    mongoDB.close()
    file.close()

    print('*'*40)
    print('已导出数据到 %s  共%d条'%(FILE_PATH, dataCount))
    print('注：如果中文乱码，请用记事本打开，然后另存为ANSI格式')
    # pause