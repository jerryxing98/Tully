from bookmark.models import Bookmark,Link
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import selector
from scrapy.http.request import Request


class BookMarkSpider(CrawlSpider):
	name="bookmark_spider"
	allowed_domains = ['aiku.me']
	start_urls=['aiku.me/explore/chart?order=all']


	#start_urls=[]
	def parse_bookmark(self,response):
		sel = Selector(response)
		bookmarks = sel.xpath('').extract

		for bookmark in bookmarks:
			yield Request('',callback=self.parse_detail)

		bookmark= Bookmark.objects.get_or_create()
		detail_url=''
		Request(baseU)


	def parse_detail(self,response):
		sel=Selector(response)
		title=sel.xpath("").extract()

		bookmark= Bookmark.objects.get_or_create(title='')

		bookmark=response.meta['bitem']
        bookmark['tag']=''
        bookmark['link']=''
        bookmark['']

    def getTitle(self,sel):
    	title=sel.xpath("").extract()
    	if not title:
    		return None
    	return title[0].strip()

    def getThumbnail(self,sel):
    	thumbnail=sel.xpath("").extract()
    	if not thumbnail:
    		return None
    	return thumbnail

    def getTags(self,sel):






    	
    	pass

    def getDescription(self,sel):
    	
    	pass