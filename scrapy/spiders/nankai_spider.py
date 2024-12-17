import scrapy
from scrapy.items import NankaiSearchEngineItem

class NankaiSpider(scrapy.Spider):
    name = 'nankai_spider'
    allowed_domains = ['nankai.edu.cn']
    start_urls = [
    'http://nankai.edu.cn',  # 南开大学首页，抓取起始点
]

def parse(self, response):
    # 抓取页面内容
    item = NankaiSearchEngineItem()
    item['title'] = response.xpath('//title/text()').get()
    item['url'] = response.url
    
    # 获取页面的所有文本内容，并去除 \n, \r, \t 等字符
    content = response.xpath('//body//text()').getall()
    cleaned_content = ' '.join(content).replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
    
    item['content'] = cleaned_content
    #item['last_modified'] = response.headers.get('Last-Modified')

    yield item

    # 继续抓取页面中的链接
    next_pages = response.xpath('//a/@href').getall()
    for next_page in next_pages:
        yield response.follow(next_page, self.parse)