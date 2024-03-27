import scrapy

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?start=' 

    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})


    def parse_job(self, response):
        jobs = response.css('li')

        for job in jobs:
            job_url = job.css(".base-card__full-link::attr(href)").get(default='not-found').strip()
            if job_url!="not-found":
                yield scrapy.Request(url=job_url, callback=self.parse_job_page)

        first_job_on_page = response.meta['first_job_on_page']
        num_jobs_returned = len(jobs)
        if num_jobs_returned > 0:
            first_job_on_page = int(first_job_on_page) + num_jobs_returned
            next_url = self.api_url + str(first_job_on_page)
            yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})

    def parse_job_page(self, response):
        yield {
            'title' : response.css('.top-card-layout__entity-info h1::text').get(default='not-found').strip(),
            'location' : response.css('.top-card-layout__entity-info h4 .topcard__flavor-row > span:nth-child(2)::text').get(default='not-found').strip(),
            'level' : response.xpath("//ul[@class='description__job-criteria-list']/li[1]/span/text()").get(default='not-found').strip(),
            'type' : response.xpath("//ul[@class='description__job-criteria-list']/li[2]/span/text()").get(default='not-found').strip(),
            'function' : response.xpath("//ul[@class='description__job-criteria-list']/li[3]/span/text()").get(default='not-found').strip(),
            'description' : response.css("div.show-more-less-html__markup").get(default='not-found').strip()
        }
