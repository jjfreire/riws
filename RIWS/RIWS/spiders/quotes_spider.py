import time
import scrapy
import re
import time

from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from RIWS.items import JobItem

class JobsSpider(scrapy.Spider):
    name = "jobs_spider"
    start_page = 1
    base_url = 'https://www.infojobs.net/ofertas-trabajo?keyword=&segmentId=&page={}&sortBy=PUBLICATION_DATE&onlyForeignCountry=false&sinceDate=ANY'
    start_urls = [
        base_url.format(start_page)
    ]
    allowed_domains = ["www.infojobs.net"]
    captcha_solved = False
    cookie_clicked = False
    max_pages = 100

    def start_requests(self):
        url = self.base_url.format(self.start_page)
        yield SeleniumRequest(
            url=url,
            callback=self.parse
        )


    def parse(self, response):
        driver = response.request.meta["driver"]

        if not self.captcha_solved:
            try:
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "geetest_radar_tip")))
                driver.find_element(By.CLASS_NAME, "geetest_radar_tip").click()
                self.captcha_solved = True

            except TimeoutException as e:
                self.logger.info("CAPTCHA not found")


        if not self.cookie_clicked:
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "didomi-notice-agree-button")))
                driver.find_element(By.ID, "didomi-notice-agree-button").click()
                self.cookie_clicked = True
                self.logger.info("Cookie consent banner clicked.")
            except TimeoutException:
                self.logger.info("Cookie consent banner not found.")

        for i in range(1, 70):
            driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(0.000025)

        selector = Selector(text=driver.page_source)

        for job_li in selector.css('main.ij-Box.ij-TemplateAdsPage-main.ij-SearchListingPageContent-list li'):
            title = job_li.css('h2.ij-OfferCardContent-description-title a::text').get()
            if title is not None:
                item = JobItem()
                item['title'] = title
                item['company'] = job_li.css('h3.ij-OfferCardContent-description-subtitle a::text').get()
                item['description'] = job_li.css('p.ij-OfferCardContent-description-description.ij-OfferCardContent-description-description--hideOnMobile::text').get()
                item['link'] = re.sub(r"^\/\/", "", job_li.css('h2.ij-OfferCardContent-description-title a::attr(href)').get())
                item['salary'] = job_li.css('span.ij-OfferCardContent-description-salary-info::text').get()
                if item['salary'] is None:
                    item['salary'] = job_li.css('span.ij-OfferCardContent-description-salary-no-information::text').get()
                
                item['duration'] = job_li.css('li.ij-OfferCardContent-description-list-item.ij-OfferCardContent-description-list-item--hideOnMobile:nth-of-type(1)::text').get()
                item['workday'] = job_li.css('li.ij-OfferCardContent-description-list-item.ij-OfferCardContent-description-list-item--hideOnMobile:nth-of-type(2)::text').get()

                item['location'] = job_li.css('span.ij-OfferCardContent-description-list-item-truncate::text').get()

                ul = job_li.css('ul.ij-OfferCardContent-description-list')
                li_elements = ul.css('li')
                li_count = len(li_elements)

                if li_count == 6:
                    item['modality'] = li_elements[1].css('::text').get()
                else:
                    item['modality'] = "No especificado"

                yield item


        current_page = int(response.url.split('page=')[-1].split('&')[0])

        if current_page < self.max_pages:
            next_page_url = self.base_url.format(current_page+1)
            yield SeleniumRequest(url=next_page_url, callback=self.parse)
