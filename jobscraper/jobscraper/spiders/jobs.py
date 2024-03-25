import scrapy

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['']
    start_urls = ['']

    def parse(self, response):
        pass
    