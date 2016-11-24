import urllib.parse
from tld import get_tld


urls = [ 'https://zhidao.baidu.com/question/367898527877597324.html',
         'http://www.jb51.net/article/55693.htm',
         'http://photo.cctv.com.cn/mlzg/',
         'https://haha.www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=python%20%20%E5%8F%96ip%E4%BA%8C%E7%BA%A7%E5%9F%9F%E5%90%8D&oq=%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F&rsv_pq=ec0fb9e40000e14a&rsv_t=b2d8%2FWrKBW%2FfBUBkTha2yoKxAG%2Fv1bnqjln4hnzR%2BXfeexw8h6WqH6BWvhw&rqlang=cn&rsv_enter=1&inputT=13463&rsv_sug3=71&rsv_sug1=56&rsv_sug7=100&rsv_sug2=0&rsv_sug4=14041',
         'http://www.cctv.com/',
         'http://tv.cctv.com/2016/10/19/VIDA1PTVlNZyU43NoUbkl3UV161019.shtml',
         'http://hahha.star.news.sohu.com/20161123/n473917589.shtml'

]
for url in urls:
    proto, rest = urllib.parse.splittype(url)
    res, rest = urllib.parse.splithost(rest)
    rest = res.replace('www.', '')
    print(rest)



print("*"*50)


for url in urls:
    try:
        print  (get_tld(url))
    except Exception as e:
        print ("unkonw")

print("*"*50)
for url in urls:
    try:
        domain = get_tld(url)
        domainStartPos = url.find(domain)
        domainEndPos = domainStartPos + len(domain)
        secondDomainStartPos = url.rfind('.', 0, domainStartPos - 1) + 1

        if secondDomainStartPos == 0:
            secondDomainStartPos = url.find('//') + 2

        secondDomain = url[secondDomainStartPos: domainEndPos]
        secondDomain = secondDomain.replace('www.', '')
        print  (secondDomain)
    except Exception as e:
        print (e)