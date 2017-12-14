import pandas as pd
from bs4 import BeautifulSoup
from urllib import parse
import pandas as pd
import re
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import asyncio

missing_movie_df = pd.read_csv('./csv/14_missing.csv', encoding='utf-8')
actor_code_bk = pd.read_csv('./ipynb/8actor_code_bak.csv', encoding='utf-8')
new_df = 0
actor_filmo = pd.DataFrame(columns=("actor_name", "filmo", "filmo_code"))

for index, row in missing_movie_df.iterrows():
    peopleNm_list = []  ### 매번 비우면서

    if '|' in getattr(row, "actor"):
        peopleNm_list = (getattr(row, "actor").split('|'))
    else:
        peopleNm_list.append(getattr(row, "actor"))

    filmoNames = getattr(row, "movieNm")
    filmocode = getattr(row, "movie_code")

    for actor in peopleNm_list:
        new_df += 1  ## actor_filmo row count
        actor_filmo.loc[new_df] = [actor, filmoNames, filmocode]


async def fetch(link, peopleNm, filmo, index):
    async with ClientSession() as session:
        async with session.get(link) as response:
            html = await response.read()
            try:
                soup = BeautifulSoup(html, "lxml")
                td = soup.find('td', class_='ellipsis')
                link = td.find('a')['onclick']
                code = int(re.search(r'\d+', link).group())  ## 코드(숫자)만 걸러내기
                total_actor_code_df.loc[index] = [peopleNm, filmo, code]
            except Exception as e:
                pass


if __name__ == "__main__":
    count = 1
    length = 300
    tasks = []
    loop = asyncio.get_event_loop()

    total_actor_code_df = pd.DataFrame(columns=['actor_name', 'filmo', 'filmo_code', 'code'])

    for index, row in actor_filmo.iterrows():

        peopleNm = getattr(row, "actor_name")
        filmo = getattr(row, "filmo")
        filmocode = getattr(row, "filmo_code")

        if any(actor_code_bk['filmo'][actor_code_bk['actor_name'] == peopleNm] == filmo):
            total_actor_code_df.loc[index] = [peopleNm,
                                              filmo,
                                              filmocode,
                                              actor_code_bk['code'][actor_code_bk['filmo'] == filmo][
                                                  actor_code_bk['actor_name'] == peopleNm].item()
                                              ]
        else:
            peopleNm_parse = parse.quote(peopleNm)
            filmo_parse = parse.quote(filmo)

            param = "sPeopleNm=%s&sMovName=%s" % (peopleNm_parse, filmo_parse)

            url1 = "http://www.kobis.or.kr/kobis/business/mast/peop/searchPeopleList.do?"

            link = url1 + param

            task = asyncio.ensure_future(fetch(link, peopleNm, filmo, index))
            tasks.append(task)

            if count == length:  ## Task 300개 채우면
                print(index)
                loop.run_until_complete(asyncio.wait(tasks))
                tasks = []
                length += 300

            count += 1

        if index == len(actor_filmo):  ## 나머지 Task 채우기
            loop.run_until_complete(asyncio.wait(tasks))
            tasks = []
            loop.close()