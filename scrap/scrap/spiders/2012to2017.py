import scrapy
import sys
from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from scrap.items import ScrapItem
from scrapy.http import Request
from scrapy.selector import Selector

sys.setdefaultencoding('utf-8')

class released_movies(scrapy.Spider):
	name = "movie_info"
	allowed_domains = ["www.kobis.or.kr"]
	urls = []
	base = 'http://www.kobis.or.kr/kobis/business/stat/offc/searchOfficHitTotList.do?'
	for i in range(1,658):
		# URL 생성
		param = 'curPage=%s&dmlMode=search&searchMode=year&searchType=&point=&standYySt=2012&standYyEd=2017&repNation=&movieNm=&openDtFr=2012-01-01&openDtTo=2017-11-30&multiMovieYn=&planType=018503&orderCond=asc&orderBy=1' % i
		urls.append(param)
	
	start_urls = urls

	def parse(self, response):
		hxs = Selector(response)
		
	
		selects = []
		selects = hxs.xpath('//table[@border="1"]/tbody/tr')
		items = []

		for select in selects:
			item = ScrapItem()
			
			movie_info = select.xpath('//td//a[@onclick]').extract()

			if 'movie' in movie_info:

#			movie_info = select.xpath('//td//a[re:test(@onclick,"\d+")])').extract()

			

			for a in select.xpath('td/a'):
			
				if 'movie' in a['onclick']:
					item['movie_name'] = select.xpath(
					item['movie_code'] = (re.search(r'\d+', a['onclick']).group())
					
		
		#	item['movie_name'] = sel.xpath('td/a')
		#	item['movie_code'] = 
		#	item['dir_name'] = 
		#	item['dir_code'] = 
		#	item['release_year'] =
		#	item['nation'] =


		
