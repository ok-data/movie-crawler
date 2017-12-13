import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# 기본 주소
base = 'http://www.kobis.or.kr/kobis/business/stat/offc/searchOfficHitTotList.do?'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; ko-KR))',
}

# 데이터 프레임 생성
movie_df = pd.DataFrame(columns=['movie_name','movie_code','director_name','director_code','release_date','nation'])
movie_df_len = 0

for i in range(1, 658):
    param = 'curPage=%s&dmlMode=search&searchMode=year&searchType=&point=&standYySt=2012&standYyEd=2017&repNation=&movieNm=&openDtFr=2012-01-01&openDtTo=2017-11-30&multiMovieYn=&planType=018503&orderCond=asc&orderBy=1' % i
    req = requests.get(base, params=param, headers=headers)

    soup = BeautifulSoup(req.content, 'html.parser')

    table = soup.find('table', border='1')
    tbody = soup.find('tbody')

    for tr in tbody.find_all('tr'):  ## html 테이블 한 행 씩
        director_code = []
        director_name = []
        temp = []
        for a in tr.find_all('a'):
            #### 영화코드
            if 'movie' in a['onclick']:
                movie_code = (re.search(r'\d+', a['onclick']).group())  ### 영화 코드만 걸르기
                movie_name = a.string

            #### 감독코드 !! 감독은 여럿일 수 있음
            if 'people' in a['onclick']:
                director_code.append(re.search(r'\d+', a['onclick']).group())
                director_name.append(a.string)
        ### 개봉일
        for td in tr.find_all('td', limit=6):
            release_year = td.string

        ### 국적
        for td in tr.find_all('td', limit=9):
            nation = td.string

        ##감독 이름,코드 , 로 조인
        dir_name = '|'.join(director_name)
        dir_code = '|'.join(director_code)

        movie_df.loc[movie_df_len] = [movie_name,
                                      movie_code,
                                      dir_name,
                                      dir_code,
                                      release_year,
                                      nation
                                      ]
        movie_df_len += 1

movie_df.to_csv("../csv/movie_default_data.csv", encoding="utf-8")