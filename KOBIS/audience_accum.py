from bs4 import BeautifulSoup
import pandas as pd
import datetime

movie_12_17 = pd.read_csv('./csv/2012-2017_kobis_movies.csv', encoding='utf-8')

# 14일차 날짜 변환
def day14_convert(release_date):
    con_release_date = datetime.datetime.strptime(release_date, "%Y-%m-%d").date()
    day14_release_date = con_release_date + datetime.timedelta(days=13)
    day14 = day14_release_date.strftime('%Y-%m-%d')
    return day14

movie_day_df = pd.DataFrame(columns=['movie_name',
                                     'movie_code',
                                     'director_name',
                                     'director_code',
                                     'nation',
                                     'release_date',
                                     'day1_date',
                                     'day1_screen',
                                     'day1_audience',
                                     'day14_date',
                                     'day14_audience'
                                    ])

df_row = 0

for row in movie_12_17.itertuples():
    try:
        movie_name = getattr(row,'movie_name')
        movie_code = getattr(row,'movie_code')
        director_name = getattr(row,'director_name')
        director_code = getattr(row,'director_code')
        nation = getattr(row,'nation')
        release_date = getattr(row,'release_date') ## %Y-%m-%d

        file = open('./KOBIS/movie_box/%s.html' % movie_code)
        soup = BeautifulSoup(file,'lxml')

        table = soup.find('table', class_='boardList02')
        tbody = table.find('tbody')

        day14_assume = day14_convert(release_date) ## 15일차 날짜

        day1_screen = 0
        day1_audience = 0
        day14_screen = 0
        day14_audience = 0


        for tr in tbody.find_all('tr'): ## 여기서 한줄씩
            tr_list = []
            for td in tr.find_all('td'): ## 한 데이터씩
                tr_list.append(td.getText())
            ################################################### 개봉일일때
            if(release_date == tr_list[0]):
                day1_date = release_date ### 개봉일
                day1_screen = tr_list[1] ### 스크린수
                day1_audience = (tr_list[9]).replace(',','') ### 당일 관객

            elif(day14_assume == tr_list[0]):
                day14_screen = tr_list[1]
                day14_audience = (tr_list[12]).replace(',','')
        movie_day_df.loc[df_row]=[movie_name,
                                  movie_code,
                                  director_name,
                                  director_code,
                                  nation,
                                  release_date,
                                  day1_date,
                                  day1_screen,
                                  day1_audience,
                                  day14_assume,
                                  day14_audience
                                 ]
        df_row +=1
        print(df_row)
    except:
        print(movie_code)
        pass
movie_day_df.to_csv("./csv/day14_movie_data.csv")