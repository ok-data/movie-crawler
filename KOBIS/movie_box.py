import requests
import pandas as pd

movie_released_df = pd.read_csv('../csv/2012-2017_kobis_movies.csv', encoding='utf-8')

base = 'http://kobis.or.kr/kobis/business/mast/mvie/searchMovieDtlXls.do?'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; ko-KR))',
}

code_list = []

code_list = movie_released_df['movie_code']

i = 0

for code in code_list:
    i += 1
    movie_code = code

    param = 'code=%s&sType=box' % movie_code

    req = requests.get(base, params=param, headers=headers)
    content = req.content
    f = open('./movie_box/%s.html' % movie_code, 'w')
    f.write(str(content))
    f.close()

    print(i)