import scrapy
from jobscraper.items import JobItem
from urllib.parse import urlencode

# API_KEY = 'bf880102-9b3a-462b-959c-01e1cfc0572f'

# def get_proxy_url(url):
#     payload = {'api_key': API_KEY, 'url': url}
#     proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
#     return proxy_url

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    # api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?start='
    countries = ['Canada', 'United States', 'United Kingdom', 'Australia', 'Germany', 'Netherlands', 'Switzerland', 'Japan', 'Singapore', 'India']
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%2BEngineering&location={country}&f_TPR=r2592000&start='

    def start_requests(self):
        for country in self.countries:
            first_job_on_page = 0
            first_url = self.api_url.format(country=country) + str(first_job_on_page)
            yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page, 'country': country})


    def parse_job(self, response):
        jobs = response.css('li')

        for job in jobs:
            job_url = job.css(".base-card__full-link::attr(href)").get(default='not-found').strip()
            if job_url!="not-found":
                yield scrapy.Request(url=job_url, callback=self.parse_job_page)

        first_job_on_page = response.meta['first_job_on_page']
        country = response.meta['country']
        num_jobs_returned = len(jobs)
        if num_jobs_returned > 0:
            first_job_on_page = int(first_job_on_page) + num_jobs_returned
            next_url = self.api_url.format(country=country) + str(first_job_on_page)
            yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page, 'country': country})

    def parse_job_page(self, response):
        job_item = JobItem()

        job_item['title'] = response.css(".top-card-layout__entity-info h1::text").get(default='not-found').strip()
        job_item['location'] = response.css(".top-card-layout__entity-info h4 .topcard__flavor-row > span:nth-child(2)::text").get(default='not-found').strip()
        job_item['level'] = response.xpath("//ul[@class='description__job-criteria-list']/li[1]/span/text()").get(default='not-found').strip()
        job_item['type'] = response.xpath("//ul[@class='description__job-criteria-list']/li[2]/span/text()").get(default='not-found').strip()
        job_item['function'] = response.xpath("//ul[@class='description__job-criteria-list']/li[3]/span/text()").get(default='not-found').strip()
        job_item['description'] = [text.strip() for text in response.css("div.show-more-less-html__markup *::text").getall()]

        yield job_item
