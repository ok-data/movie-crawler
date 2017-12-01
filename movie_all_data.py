import requests
import os
import re

base = 'http://www.kobis.or.kr/kobis/business/stat/offc/searchOfficHitTotList.do?'

for i in range(1, 658):
    param = 'curPage=%s&dmlMode=search&searchMode=year&searchType=&point=&standYySt=2012&standYyEd=2017&repNation=&movieNm=&openDtFr=2012-01-01&openDtTo=2017-11-30&multiMovieYn=&planType=018503&orderCond=asc&orderBy=1' % i
    req = requests.get(base, params=param)
    content = req.text
    f = open('./movie_lists_html/%s.html' % i, 'w')
    f.write(content)
    f.close()
    print(i,end='\r')
