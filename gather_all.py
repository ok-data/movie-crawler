import pandas as pd

movie_day14_df = pd.read_csv('./csv/director14.csv', encoding='utf-8')

final_df = pd.read_csv('./csv/14actor_avg.csv', encoding='utf-8')

missing_movie_df = pd.read_csv('./csv/14_missing.csv', encoding='utf-8')

actor_sum = pd.DataFrame(columns=['movie_name',
                                  'nation',
                                  'distribution',
                                  'director_average',
                                  'actor_sum',
                                  'rate',
                                  'genre',
                                  'release_date',
                                  'day1_screen',
                                  'day1_audience',
                                  'day14_date',
                                  'day14_audience'
                                  ])

for index, row in movie_day14_df.iterrows():
    movie_name = getattr(row, 'movie_name')
    movie_code = getattr(row, 'movie_code')
    director_average = getattr(row, 'director_average')
    nation = getattr(row, 'nation')
    release_date = getattr(row, 'release_date')
    day1_screen = getattr(row, 'day1_screen')
    day1_audience = getattr(row, 'day1_audience')
    day15_date = getattr(row, 'day14_date')
    day15_audience = getattr(row, 'day14_audience')

    movie_name = movie_name[1:]

    try:
        actor_sum.loc[index] = [
            movie_name,  # 'movie_name',
            nation,  # 'nation',
            missing_movie_df['distribution'][missing_movie_df['movie_code'] == movie_code].item(),  ## 배급사
            director_average,  # 'director_sum',
            sum(final_df['average_audience'][final_df['movie_code'] == movie_code]),  # 'actor_sum'
            missing_movie_df['rate'][missing_movie_df['movie_code'] == movie_code].item(),  # 'rate',
            missing_movie_df['genre'][missing_movie_df['movie_code'] == movie_code].item(),  # 'genre',
            release_date,  # 'release_date'
            day1_screen,  # 'day1_screen',
            day1_audience,  # day1_audience
            day15_date,
            day15_audience
        ]
    except Exception as e:
        print(movie_name, index)
        print(e)