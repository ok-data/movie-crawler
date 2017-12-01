import pandas as pd
from pytrends.request import TrendReq

final = pd.read_csv('./csv/14_final.csv')

# date=2015-02-01%202015-03-01&geo=KR&q=%ED%82%B9%EC%8A%A4%EB%A7%A8

base = 'https://trends.google.co.kr/trends/explore?cat=34&'

pytrend = TrendReq()

for index, row in final.iterrows():
    movie_name = getattr(row, 'movie_name')
    nation = getattr(row, 'nation')
    distribution = getattr(row, 'distribution')
    director_average = getattr(row, 'director_average')
    actor_sum = getattr(row, 'actor_sum')
    rate = getattr(row, 'rate')
    genre = getattr(row, 'genre')
    release_date = getattr(row, 'release_date')
    day1_screen = getattr(row, 'day1_screen')
    day1_audience = getattr(row, 'day1_audience')
    day14_date = getattr(row, 'day15_date')
    day14_audience = getattr(row, 'day15_audience')

    pytrend.build_payload(kw_list=[movie_name, '영화'],timeframe='%s %s' % (release_date,day14_date), geo='KR', cat='34')

    interest_time_over_time = pytrend.interest_over_time()

