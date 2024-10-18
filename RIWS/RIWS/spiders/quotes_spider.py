import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from RIWS.items import JobItem


class JobsSpider(CrawlSpider):
    name = "jobs_spider"
    start_page = 1
    base_url = 'https://www.infojobs.net/ofertas-trabajo?keyword=&segmentId=&page={}&sortBy=PUBLICATION_DATE&onlyForeignCountry=false&sinceDate=ANY'.format(start_page)
    start_urls = [
        base_url
    ]
    # rules = (
    #     Rule(LinkExtractor(allow=r'/regex/'), callback='parse_item', follow=True),
    # )

    # Resolver problema de que non cargan todos ao principio

    def parse(self, response):
        #for job_li in response.xpath('//div[contains(@class, "ij-Box") and contains(@class, "ij-TemplateAdsPage-main") and contains(@class, "ij-SearchListingPageContent-list")]'):
        for job_li in response.css('main.ij-Box.ij-TemplateAdsPage-main.ij-SearchListingPageContent-list'):
            item = JobItem()
            item['title'] = job_li.css('h2.ij-OfferCardContent-description-title a::text').get()
            item['company'] = job_li.css('h3.ij-OfferCardContent-description-subtitle a::text').get()
            item['description'] = job_li.css('p.ij-OfferCardContent-description-description.ij-OfferCardContent-description-description--hideOnMobile::text').get()
            #item['title'] = job_li.xpath('.//h2[contains(@class, "ij-OfferCardContent-description-title")]/a/text()').get()
            #item['company'] = job_li.xpath('.//h3[contains(@class, "ij-OfferCardContent-description-subtitle")]/a/text()').get()
            #item['description'] = job_li.xpath('.//div[contains(@class, "ij-OfferCardContent-description-description") and contains(@class, "ij-OfferCardContent-description-description--hideOnMobile")]/text()').get()

            yield item


        current_page = int(response.url.split('page=')[-1].split('&')[0])
        max_pages = 10

        if current_page < max_pages:
            next_page_url = self.base_url.format(current_page+1)
            yield scrapy.Request(next_page_url, callback=self.parse)