import time
import scrapy
import re
import time
import os
import json

from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
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

    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)

    max_pages = min(config.get('max_pages', 100), 400)  # 100 por defecto, 400 como máximo

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
                def set_salary_vars(item, salary):
                    min_salary = None
                    max_salary = None

                    """
                    Explicación de la regex:
                        Primer grupo de captura: (\d+(?:\.\d{3})*)
                            \d+               -> Uno o más dígitos
                            (?:\.\d{3})*      -> Grupo NO capturador que permite un punto seguido de (exactamente) 3 dígitos
                                *             -> El asterisco permite que ese patrón se repita 0 o más veces

                            El grupo no capturador se utiliza para usar un patrón que queremos hacer que coincida con 
                            partes de la cadena pero sin capturar esas coincidencias como grupos separados adicionales.

                        Segundo grupo de captura: (?:.*?(\d+(?:\.\d{3})*))?
                            ?:.*?             -> Grupo NO capturador que ignora cualquier texto entre los dos números, coincidiendo con 
                                                 la menor cantidad posible de caracteres antes de buscar el siguiente número 
                                                 (*?, non-greedy)
                            (\d+(?:\.\d{3})*) -> Mismo grupo de captura que el "Primer grupo de captura". Explicación arriba.
                            ?                 -> Hace que el segundo número sea opcional, por lo que puede únicamente estar presente un número.
                        
                    """
                    regex = r'(\d+(?:\.\d{3})*)(?:.*?(\d+(?:\.\d{3})*))?'

                    if salary:
                        match = re.search(regex, salary)
                        if match:
                            # Capturar el primer número (siempre presente si hay match)
                            min_value = int(match.group(1).replace('.', ''))
                            # Capturar el segundo número (si existe)
                            max_value = int(match.group(2).replace('.', '')) if match.group(2) else min_value
                            
                            if 'mes' in salary.lower():
                                min_salary, max_salary = min_value*12, max_value*12
                            else:
                                min_salary, max_salary = min_value, max_value

                    item['min_salary'] = min_salary
                    item['max_salary'] = max_salary                  
                
                item = JobItem()
                item['title'] = title
                item['company'] = job_li.css('h3.ij-OfferCardContent-description-subtitle a::text').get()
                item['description'] = job_li.css('p.ij-OfferCardContent-description-description.ij-OfferCardContent-description-description--hideOnMobile::text').get()
                item['link'] = 'https://' + re.sub(r"^\/\/", "", job_li.css('h2.ij-OfferCardContent-description-title a::attr(href)').get())
                salary = job_li.css('span.ij-OfferCardContent-description-salary-info::text').get()
                if salary is None:
                    salary = job_li.css('span.ij-OfferCardContent-description-salary-no-information::text').get()
                set_salary_vars(item, salary)
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

                item['image'] = job_li.css('img.sui-AtomImage-image').attrib['src']
                yield item


        current_page = int(response.url.split('page=')[-1].split('&')[0])

        if current_page < self.max_pages:
            next_page_url = self.base_url.format(current_page+1)
            yield SeleniumRequest(url=next_page_url, callback=self.parse)
