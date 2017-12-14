import aiohttp
import asyncio
import lxml
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import pandas as pd

total_actor_code_df = pd.read_csv('./csv/14_actor_code.csv', encoding='utf-8')

async def fetch(link, director_code, filmo_name, index, movie_code):
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
                elif any('주연' in x for x in list(count.strings)):
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
    count = 1
    length = 300
    tasks = []
    last = 0
    director_average_df = pd.DataFrame(columns=['code', 'filmo', 'movie_code', 'average_audience'])

    loop_director = asyncio.get_event_loop()

    for index, row in total_actor_code_df.iterrows():
        filmo_name = getattr(row, 'filmo')
        director_code = getattr(row, 'code')
        movie_code = getattr(row, 'filmo_code')

        param = "code=%s&sType=filmo" % (director_code)

        url1 = "http://www.kobis.or.kr/kobis/business/mast/peop/searchPeopleDtl.do?"

        link = url1 + param

        task = asyncio.ensure_future(fetch(link, director_code, filmo_name, index, movie_code))
        tasks.append(task)

        if index == length:
            print(index)
            loop_director.run_until_complete(asyncio.wait(tasks))
            tasks = []
            length += 300

        if index == len(total_actor_code_df):
            loop_director.run_until_complete(asyncio.wait(tasks))
            tasks = []
            loop_director.close()