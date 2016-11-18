# enconding = utf8
import pymongo
from pymongo.collection import Collection
import sys
sys.path.append("..")
from utils.log import log

MONGO_HOST = 'localhost'
MONGO_PORT = 27017

FILE    = 'D:\\ku6_todo.csv'
WEBSITE = "酷六"

class MongoDB():
    def __init__(self, db = '', host = MONGO_HOST, port = MONGO_PORT):
        self.host = host
        self.port = port
        self.db = db

    def getMongoDB(self):
        try:
            self.client = pymongo.MongoClient(self.host, self.port)
            db = self.db
            self.db = self.client.crawl  #这需要手动填mongodb数据库名
            return self.db
        except:
            print('connect mongodb error.')

    def close(self):
        self.client.close()

# 纪录片表 `documentary`

# | 字段名              | 数据类型| 长度 | 说明       | 描述 |
# |:-------------------|:-------|:----|:----------|:----|
# |doc_name||||片名|
# |episode_num||||集数|
# |abstract||||简介|
# |play_num||||总播放量|
# |url||||纪录片url|
# |total_length||||总片长 (单位秒)|
# |institutions||||播出机构|
# |release_time||||发布时间|
# |cyclopedia_msg||||百度百科上的信息|
# |website_id||||网站id|

if __name__ == '__main__':
    dataCount = 0

    mongoDB = MongoDB()
    db = mongoDB.getMongoDB()

    website = list(db.website.find({'web_name':WEBSITE}))
    assert len(website), '数据库中无%s信息'%WEBSITE
    websiteId = website[0]['_id']

    file = open(FILE, 'w+',  encoding='utf8')
    file.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%('片名', '集数', '简介', '播放量', 'url', '片长', '播出机构', '发布时间', '百科信息', '网站'))
    flag = True
    while flag:
        flag = False
        datas = db.documentary.find({'website_id':websiteId})
        for data in datas:
            print('正在导出 %s'%data['doc_name'])
            value = (data['doc_name'], data['episode_num'], data['abstract'], data['play_num'], data['url'], data['total_length'], data['institutions'], data['release_time'], data['cyclopedia_msg'], WEBSITE)
            file.write('"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"\n'%value)
            dataCount = dataCount + 1


    mongoDB.close()
    file.close()

    print('*'*40)
    print('已导出数据到 %s  共%d条'%(FILE, dataCount))
    print('注：如果中文乱码，请用记事本打开，然后另存为ANSI格式')
    # pause