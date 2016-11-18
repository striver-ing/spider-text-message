# encoding=utf8
import logging
import os

projectName = 'spider-text-message'
currentPath = os.path.abspath('.')
projectPath = currentPath[:currentPath.find(projectName) + len(projectName)]

logging.basicConfig(level=logging.DEBUG,
    format='%(thread)d %(threadName)s %(asctime)s %(filename)s %(funcName)s [line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%b-%d %H:%M:%S',
    filename=projectPath+'\\log\\%s.log'%projectName,
    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(thread)d %(threadName)s %(asctime)s %(filename)s %(funcName)s [line:%(lineno)d] %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

log = logging

#日志级别大小关系为：critical > error > warning > info > debug