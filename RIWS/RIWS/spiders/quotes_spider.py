import time
import scrapy
import re
import cv2
import time
import numpy as np
from PIL import Image
import urllib.request
import matplotlib.pyplot as plt

from random import randint

from scipy import ndimage, misc

from captcha_funcs import *

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
                # time.sleep(10)
                self.captcha_solved = True
                image_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "geetest_item_wrap")))
                time.sleep(1)
                outer_html = image_element.get_attribute('outerHTML')
                image_url = re.sub(r'.*url\(&quot;(https?://.+?)&quot;\).*', r'\1', outer_html)
                
                image_path = 'captcha.jpg'
                urllib.request.urlretrieve(image_url, image_path)
                img_grey = cv2.imread(image_path,0)
                Image.fromarray(img_grey)
                
                main_pane = img_grey[:350,:]

                color_threshold = 180
                main_pane = cv2.blur(main_pane,(3,3)) # By blurring, we can remove some white pixels which may affecting the matching
                main_pane[main_pane<color_threshold] = 0
                main_pane[main_pane>=color_threshold] = 255
                Image.fromarray(main_pane)

                icons_rect_coordinates = find_bounding_box(main_pane, (20,20), (100,100),sort=False)
                icons = segment_pictures(main_pane,icons_rect_coordinates,(30,30))

                draw_bounding_box(main_pane, icons_rect_coordinates)

                target_color_threshold = 40
                target_pane = 255 - img_grey[350:,:]
                target_pane[target_pane<target_color_threshold] = 0
                target_pane[target_pane>=target_color_threshold] = 255

                Image.fromarray(target_pane)

                targets_rect_coordinates = find_bounding_box(target_pane, (5,5), (100,100)) 
                targets = segment_pictures(target_pane,targets_rect_coordinates,(30,30))
                draw_bounding_box(target_pane, targets_rect_coordinates)

                def calculate_max_matching(target,icon,d):
                    largest_val = 0
                    for degree in range(0,360,d):
                        tmp = ndimage.rotate(target, degree, reshape=False)
                        res = cv2.matchTemplate(icon,tmp,cv2.TM_CCOEFF_NORMED)
                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                        if max_val > largest_val:
                            largest_val = max_val
                    return largest_val
                
                similarity_matrix = []
                for target in targets:
                    similarity_per_target = []
                    for icon in icons:
                        similarity_per_target.append(calculate_max_matching(target,icon,6))
                    similarity_matrix.append(similarity_per_target)

                fig,ax = plt.subplots(1)
                ax.imshow(main_pane)

                # Calculate Mapping
                target_candidates = [False for _ in range(len(targets))]
                icon_candidates = [False for _ in range(len(icons))]

                mapping = {}

                arr = np.array(similarity_matrix).flatten()
                arg_sorted = np.argsort(-arr)

                for e in arg_sorted:
                    col = e //len(icons)
                    row = e % len(icons)
                    
                    if target_candidates[col] == False and icon_candidates[row] == False:
                        target_candidates[col], icon_candidates[row] = True, True
                        mapping[col] = row

                color_map = {1:'b',2:'r',3:'y',4:'g'}
                for key in mapping:
                    x,y,w,h = icons_rect_coordinates[mapping[key]]
                    
                    # x,y is the coordinate of top left hand corner
                    # Bounding box is 70x70, so centre of circle = (x+70/2, y+70/2), i.e. (x+35, y+35)
                    centre_x = x+(w//2)
                    centre_y = y+(h//2)
                    # Plot circle
                    circle = plt.Circle((centre_x,centre_y), 20, color=color_map[key+1], fill=False, linewidth=5)
                    # Plot centre
                    plt.plot([centre_x], [centre_y], marker='o', markersize=10, color="white")
                    ax.add_patch(circle)

                plt.savefig("output_image_with_bounding_boxes.png")
                Image.fromarray(img_grey[350:,:110]) 

                time.sleep(5)
                # for i, target in enumerate(targets):
                #     key = i
                #     x,y,w,h = icons_rect_coordinates[mapping[key]]
                    
                #     # x,y is the coordinate of top left hand corner
                #     # Bounding box is 70x70, so centre of circle = (x+70/2, y+70/2), i.e. (x+35, y+35)
                #     centre_x = x+(w//2)
                #     centre_y = y+(h//2)
                    
                #     ele = driver.find_element(By.CLASS_NAME, "geetest_item_img")
                #     action = webdriver.common.action_chains.ActionChains(driver)
                #     action.move_to_element_with_offset(ele, centre_x, centre_y)
                #     time.sleep(randint(100,700)/1000)
                #     action.click()
                #     action.perform()


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

                # item['location']
                # item['modality']
                yield item


        current_page = int(response.url.split('page=')[-1].split('&')[0])
        max_pages = 5

        if current_page < max_pages:
            next_page_url = self.base_url.format(current_page+1)
            yield SeleniumRequest(url=next_page_url, callback=self.parse)
