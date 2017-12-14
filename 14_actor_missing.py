import pandas as pd
import requests
import random

movie_day8_df = pd.read_csv('./csv/day14_movie_data.csv', encoding='utf-8')

page_type = "movie"  #
search_type = "searchMovieInfo"
return_type = "json"

key_list = ['a0c311535c77ebdb3bab229d4955a54a',
            '797849ae4ee295a5b81f0b5628e37931',
            '206a3a64108e08359f4de77e77de1c4d',
            '0f56b7a37c358fa8fd15a4ffe5f78ab3',
            '16cc45cd8569a777e530e4c26e2c474f'
            ]
base = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/"

missing_movie_df = pd.DataFrame(columns=['movieNm', 'movie_code', 'nations', 'distribution', 'rate', 'genre', 'director', 'actor', 'cast'])
row = 0

code = movie_day8_df['movie_code']

for movie_code in code:
    row += 1
    param = "&movieCd=%s" % movie_code

    request_token = page_type + "/" + search_type + "." + return_type + "?key=" + random.choice(key_list)

    full_url = base + request_token + param

    rep = requests.get(full_url)

    movie_data = rep.json()

    ##국적값 nations
    temp = []
    for item in movie_data["movieInfoResult"]["movieInfo"]["nations"]:
        temp.append(str(item.get("nationNm")))
        nations = "|".join(temp)

    ##장르값 genres
    temp = []
    for item in movie_data["movieInfoResult"]["movieInfo"]["genres"]:
        temp.append(str(item.get("genreNm")))
        genre = "|".join(temp)

    ##배우, 캐스트
    temp = []
    cast = []
    for item in movie_data["movieInfoResult"]["movieInfo"]["actors"]:
        temp.append(str(item.get("peopleNm")))
        cast.append(str(item.get("cast")))
        cast = list(filter(None, cast))
        actor_name = "|".join(temp)
        cast_name = "|".join(cast)

    ##감독값 director_name
    temp = []
    for item in movie_data["movieInfoResult"]["movieInfo"]["directors"]:
        temp.append(str(item.get("peopleNm")))
        director_name = "|".join(temp)

    temp = []
    for item in movie_data["movieInfoResult"]["movieInfo"]["companys"]:
        if str(item.get("companyPartNm")) == "배급사":
            temp.append(str(item.get("companyNm")))
        distribution = "|".join(temp)

    ##등급값 rate
    temp = []
    for item in movie_data["movieInfoResult"]["movieInfo"]["audits"]:
        temp.append(str(item.get("watchGradeNm")))
        rate = "|".join(temp)

    missing_movie_df.loc[row] = [movie_data["movieInfoResult"]["movieInfo"]["movieNm"],
                                 movie_code,
                                 nations,
                                 distribution,
                                 rate,
                                 genre,
                                 director_name,
                                 actor_name,
                                 cast_name
                                 ]
    print(row, end='\r')