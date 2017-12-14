import pandas as pd

# day15_with_news = pd.read_csv('./csv/15_final_with_news.csv', encoding='euc-kr')
day15_with_news = pd.read_csv('./csv/15_final.csv', encoding='utf-8')

day14_final = pd.read_csv('./csv/day14_movie_data.csv', encoding='utf-8')

day14_date_ls = []
day14_audience_ls = []

for i in day15_with_news['movie_name']:
    try:
        day14_date_ls.append(day14_final['day14_date'][day14_final['movie_name'] == i].item())

        day14_audience_ls.append(day14_final['day14_audience'][day14_final['movie_name'] == i].item())
    except:
        day14_date_ls.append('0')
        day14_audience_ls.append('0')
        print(i)

day15_with_news['day14_date'] = day14_date_ls
day15_with_news['day14_audience'] = day14_date_ls
