import scrapy
from scrapy.spiders import SitemapSpider
import pymongo
# from pymongo import MongoClient
client = pymongo.MongoClient('localhost',27017)
db = client['database_name']
class Myspider(SitemapSpider):
    name = 'spidername'
    sitemap_urls = ['https://www.example.com/sitemap.xml','http://www.example.com/image-sitemap.xml']
    sitemap_rules = [
        ('/carddetails/', 'parse'),
        # ('/category/', 'parse_category'),
    ]
    def parse(self,response):
            title = response.css('h1.productlabel.hidden-xs::text').extract_first()
            category  =  response.css('body > div.page > section:nth-child(4) > ol > li:nth-child(3) > a::text').extract_first()
            describe = response.xpath('/html/body/div[3]/div[2]/div[1]/section[1]/div/div[2]/div[1]/div[1]/p/text()').extract()
            try:
                price  = response.css('.productprice::text').extract_first()[4:]
            except:
                price = response.css('.productprice::text').extract_first()
            image_url = ['https://www.parekhcards.com' + str(i) for i in response.css('#thumb ul  li  a::attr(href)').extract()]
            lists = response.css('.moreinfo tr td *::text').extract()
            lists = [i.strip().replace(':','') for i in lists]
            lists_data = []
            for j in range(0,len(lists)-1,2):
                lists_data.append((lists[j],lists[j+1]))
            description = dict(lists_data)
            description['describe'] = describe
            name = response.css('ul.commentslist .comment-title::text').extract()
            testimonial = response.css('ul.commentslist comment-text::text').extract()
            lists = []
            for tuples in zip(name,testimonial):
                lists.append(tuples)
            review = dict(lists)
            if title == '' or title == 'None' or title == [] or title == None:
                pass
            else:
                db[category].insert({'title':title,'price':price,'description':description,'review':review,'image_url':image_url,'ref_links':response.url})
            print(lists)
	#def parse_category(self,response):

# #import the scrapy module
# import scrapy
# #import the scrapy sitemapSpider
# from scrapy.spiders import SitemapSpider
# # import pymongo to store the data in mongodb
# import pymongo
# # from pymongo import MongoClient
# # initialize the Mongoclient
# client = pymongo.MongoClient(‘localhost’,27017)
# # creating the database
# db = client[‘database_name’]
# class Myspider(SitemapSpider):
#       name = ‘spidername’
#       # set the sitemap url in sitemap_urls predefined variables
#       sitemap_urls =      [‘https://www.example.com/sitemap.xml','http://www.example.com/image-sitemap.xml']
#
#  sitemap_rules = [
#  (‘/carddetails/’, ‘parse’),
#  ]
#
#  def parse(self,response):
#      title = response.css(‘h1.productlabel.hidden-   xs::text’).extract_first()
#      category = response.css(‘body > div.page > section:nth-child(4) > ol > li:nth-child(3) > a::text’).extract_first()
#      describe = response.xpath(‘/html/body/div[3]/div[2]/div[1]/section[1]/div/div[2]/div[1]/div[1]/p/text()’).extract()
#      try:
#        price = response.css(‘.productprice::text’).extract_first()[4:]
#      except:
#        price = response.css(‘.productprice::text’).extract_first()
#      image_url = [‘https://www.parekhcards.com’ + str(i) for i in response.css(‘#thumb ul li a::attr(href)’).extract()]
#      lists = response.css(‘.moreinfo tr td *::text’).extract()
#      lists = [i.strip().replace(‘:’,’’) for i in lists]
#      lists_data = []
#      for j in range(0,len(lists)-1,2):
#         lists_data.append((lists[j],lists[j+1]))
#      description = dict(lists_data)
#      description[‘describe’] = describe
#      name = response.css(‘ul.commentslist .comment-   title::text’).extract()
#      testimonial = response.css(‘ul.commentslist comment-text::text’).extract()
#      lists = []
#      for tuples in zip(name,testimonial):
#         lists.append(tuples)
#      review = dict(lists)
#      if title == ‘’ or title == ‘None’ or title == [] or title == None:
#         pass
#      else:        db[category].insert
# ({‘title’:title,’price’:price,’description’:descr
# iption,’review’:review,’image_url’:image_url,’ref_links’:response.url})
# import requests
# import string
# PAGE_SIZE = 15
# url = 'http://example.webscraping.com/ajax/' + 'search.json?page={}&page_size={}&search_term=a'
# countries = set()
# for letter in string.ascii_lowercase:
#    print('Searching with %s' % letter)
#    page = 0
#    while True:
#        response = requests.get(url.format(page, PAGE_SIZE, letter))
#        data = response.json()
#        print('adding %d records from the page %d' %(len(data.get('records')),page))
#    for record in data.get('records'):countries.add(record['country'])
#    page += 1
#    if page >= data['num_pages']:
#       break
#    with open('countries.txt', 'w') as countries_file:
#        countries_file.write('n'.join(sorted(countries)))
