from ..items import RetiDataItem
import scrapy
from scrapy.crawler import CrawlerProcess

URL = 'https://reti.vn/projects'

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [URL]

    def parse(self, response):
        for page_link in response.xpath('//div[@class="card-body p-2"]/a/@href').getall():
            proj_page = response.urljoin(page_link)
            yield scrapy.Request(proj_page, callback=self.parse_single_proj)
                
        next_page = response.css('ul.pagination li a')[-1].attrib
        if "next" in next_page.values():
            next_page_link = response.urljoin(next_page.get('href'))
            yield scrapy.Request(next_page_link, callback=self.parse)

    def parse_single_proj(self, response):
        info_department = response.xpath('//div[@class="info-department"]')
        item = RetiDataItem(
            address = info_department.xpath('//span[@class="address"]/text()').get(),
            department = info_department.xpath('//h3[@class="department-name ml-0 pt-2"]/text()').get(), 
            price = info_department.xpath('//div[@class="price-department ml-0"]/span/text()').getall(),
            area = info_department.xpath('//div[@class="acreage col-6 pl-0 ml-0"]/span/text()').get(),
            group = info_department.xpath('//div[@class="sun-group col-6"]/span/text()').getall(),  
            amount = {
                "remain" : info_department.xpath('//div[@class="amount col-6 pl-0"]/span/text()')[1].get(), 
                "total" : info_department.xpath('//div[@class="amount col-6 pl-0"]/span/text()')[3].get() 
            },
            subdivision = {
                "type" : info_department.xpath('//div[@class="floor col-6"]/span/text()')[1].get(),
                "buildings" : info_department.xpath('//div[@class="floor col-6"]/span/text()')[3].get()
            }
        )
        yield item


# process = CrawlerProcess(settings={
#     "FEEDS": {
#         "data4.json": {"format": "json"},
#     },
# })

# process.crawl(QuotesSpider)
# process.start()


