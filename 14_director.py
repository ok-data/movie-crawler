import pandas as pd
import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup

movie_day15_df = pd.read_csv('csv/day14_movie_data.csv', encoding='utf-8')

director_filmo = pd.DataFrame(columns=("code", "filmo", "movie_code"))

new_df = 0
for index, row in movie_day15_df.iterrows():
    try:
        peopleNm_list = []  ### 매번 비우면서

        if '|' in getattr(row, "director_name"):
            peopleNm_list = (getattr(row, "director_code").split('|'))
        else:
            peopleNm_list.append(getattr(row, "director_code"))

        filmoNames = getattr(row, "movie_name")
        filmocode = getattr(row, "movie_code")
        for director in peopleNm_list:
            new_df += 1  ## actor_filmo row count
            director_filmo.loc[new_df] = [director, filmoNames, filmocode]
        print(index)
    except:
        print(index,getattr(row,'director_code'))
        pass


async def fetch(link, director_code, filmo_name, movie_code, index):
    async with ClientSession() as session:
        async with session.get(link) as response:
            html = await response.read()

            soup = BeautifulSoup(html, "lxml")

            tbody = soup.findAll('em', class_='tl')

            result = []

            for page in soup.find_all('p', class_='pageList pmt2'):
                page_num = list(page.strings)
                page_result = [i for i in page_num if i != '\n']

            for etcParam in page_result:
                url2 = "http://www.kobis.or.kr/kobis/business/mast/peop/searchPeopleDtl.do?"

                param = "code=%s&sType=filmo&etcParam=%s" % (director_code, etcParam)

                link = url2 + param

                average = await get(link, filmo_name, result)

                director_average_df.loc[index] = [director_code,
                                                  filmo_name,
                                                  movie_code,
                                                  average
                                                  ]


async def get(link, filmo_name, result):
    async with ClientSession() as session:
        async with session.get(link) as response:

            html = await response.read()

            soup = BeautifulSoup(html, "lxml")

            tr_tag = []
            real_tag = []
            for count in soup.findAll('dl'):
                if any(filmo_name in s for s in list(count.strings)):
                    pass
                elif any('감독' in x for x in list(count.strings)):
                    #                 else:
                    tr_tag = tr_tag + list(count.strings)

            for elem in range(0, len(tr_tag)):
                if tr_tag[elem] == '[공식통계]':
                    real_tag.append(tr_tag[elem + 3])

            real_tag = [w.replace('명', '') for w in real_tag]  ## 명 없애기
            real_tag = [w.replace(',', '') for w in real_tag]  ## , 없애기
            #             real_tag = [w.replace('','0') for w in real_tag] ## , 없애기
            real_tag = list(filter(None, real_tag))  ## 빈값 지우기
            real_tag = list(map(int, real_tag))

            result.extend(real_tag)

            return int(average(result))


def average(values):
    if len(values) == 0:
        return 0
    return sum(values, 0.0) / len(values)


if __name__ == "__main__":

    length = 300
    tasks = []

    director_average_df = pd.DataFrame(columns=['code', 'filmo', 'movie_code', 'average_audience'])

    loop_director = asyncio.get_event_loop()

    for index, row in director_filmo.iterrows():
        filmo_name = getattr(row, 'filmo')
        filmo_name = filmo_name[1:]
        director_code = getattr(row, 'code')
        movie_code = getattr(row, 'movie_code')
        param = "code=%s&sType=filmo" % (director_code)

        url1 = "http://www.kobis.or.kr/kobis/business/mast/peop/searchPeopleDtl.do?"

        link = url1 + param

        task = asyncio.ensure_future(fetch(link, director_code, filmo_name, movie_code, index))
        tasks.append(task)

        if index == length:
            print(index)
            loop_director.run_until_complete(asyncio.wait(tasks))
            tasks = []
            length += 300

        if index == len(director_filmo):
            loop_director.run_until_complete(asyncio.wait(tasks))
            tasks = []
            loop_director.close()

            director_sum = pd.DataFrame(columns=['movie_name', 'director_average'])

