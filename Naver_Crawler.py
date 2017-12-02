import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup
import time
import random

movie_data = pd.read_csv("./csv/15_final.csv", encoding='utf-8')
director_data = pd.read_csv("./ipynb/15_missing.csv", encoding='utf-8')

movie_name = [i for i in movie_data['movie_name']]
release_date = [i for i in movie_data['release_date']]
end_date = [i for i in movie_data['day15_date']]
director_name = []

for i in movie_name:
    print(i)
    director_name.append(director_data['director'][director_data['movieNm'] == i].item())

Search=zip(movie_name,director_name)

Plus=[]
for i in Search:
    a = list(i)
    Plus.append(a)

MovieDirector=[]
for i in Plus:
    b=' '.join(i)
    MovieDirector.append(b)

Movie_date = pd.DataFrame()
Movie_date['movie_name'] = MovieDirector
Movie_date['release_date'] = release_date
Movie_date['day15_date'] = end_date


# 링크 틀
def url_maker(query, sdate, edate):
    # base_url = 'http://news.naver.com/main/search/search.nhn?query={}&ds={}&de={}'
    # base_url = 'https://search.naver.com/search.naver?where=news&query={}&ds={}&de={}'
    base_url = 'https://search.naver.com/search.naver?where=news&query={}&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds={}&de={}'
    con_sdate = datetime.datetime.strptime(sdate, "%Y-%m-%d").date()
    con_edate = datetime.datetime.strptime(edate, "%Y-%m-%d").date()

    sdate = con_sdate - datetime.timedelta(days=7)
    edate = con_edate - datetime.timedelta(days=7)

    sdate = sdate.strftime('%Y.%m.%d')
    edate = edate.strftime('%Y.%m.%d')

    encoded_query = requests.utils.quote(query)
    base_url = base_url.format(encoded_query, sdate, edate)

    return base_url


# 최종 링크주소 새성
FinalUrl = []
for index, row in Movie_date.iterrows():
    movie_name = getattr(row, 'movie_name')
    release_date = getattr(row, 'release_date')
    end_date = getattr(row, 'day15_date')

    url = url_maker(movie_name, release_date, end_date)

    FinalUrl.append(url)

# user-agent 헤더를 넣어야 제한 안걸림
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; ko-KR))',
}

countlist = []
i = 0
for url in FinalUrl:
    try:
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        cnt = soup.find('div', class_='title_desc all_my').text
        cnt = cnt[7:-1]
        cnt = cnt.replace(',', '')
        if cnt == '':
            cnt = '0'
        i += 1
        print(cnt + ": %s" % i)

    except Exception as e:
        print(url)
        print(e)
        cnt = '0'
        pass
    countlist.append(cnt)

    # time.sleep(2 + random.random() * 4)

movie_data['news7'] = countlist

movie_data.to_csv('./csv/15_final_with_news.csv', encoding='euc-kr')
