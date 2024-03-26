import scrapy

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?start=' 

    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})


    def parse_job(self, response):
        # job_item = {}
        jobs = response.css('li')

        for job in jobs:

            yield {
                'job_title' : job.css("h3::text").get(default='not-found').strip(),
                'job_url': job.css(".base-card__full-link::attr(href)").get(default='not-found').strip(),
                'job_location': job.css('.job-search-card__location::text').get(default='not-found').strip()
            }
            
            # job_item['job_title'] = job.css("h3::text").get(default='not-found').strip()
            # job_item['job_detail_url'] = job.css(".base-card__full-link::attr(href)").get(default='not-found').strip()
            # # job_item['job_listed'] = job.css('time::text').get(default='not-found').strip()   
            # # job_item['company_name'] = job.css('h4 a::text').get(default='not-found').strip()
            # # job_item['company_link'] = job.css('h4 a::attr(href)').get(default='not-found')
            # job_item['company_location'] = job.css('.job-search-card__location::text').get(default='not-found').strip()
            # yield job_item
        
        first_job_on_page = response.meta['first_job_on_page']

        num_jobs_returned = len(jobs)
        # print("******* Num Jobs Returned *******")
        # print(num_jobs_returned)
        # print('*****')

        if num_jobs_returned > 0:
            first_job_on_page = int(first_job_on_page) + num_jobs_returned
            next_url = self.api_url + str(first_job_on_page)
            yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})

    
