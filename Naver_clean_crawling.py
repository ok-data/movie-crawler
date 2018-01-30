import requests
from bs4 import BeautifulSoup

url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=%EA%B3%A1%EC%84%B1+%EB%82%98%ED%99%8D%EC%A7%84&oquery=%EA%B3%A1%EC%84%B1+%EB%82%98%ED%99%8D%EC%A7%84&tqi=TFt3wdpySD0ssvkgAFCssssstbh-278429"

header = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; ko-KR))',
}

try:
    req = requests.get(url, headers=header)
    soup = BeautifulSoup(req.content, 'html.parser')
    data = soup.find('div', class_='title_desc all_my').text
    data = data[7:-1]
    data = data.replace(',', '')
    print(data)
except Exception as e:
    print(e)