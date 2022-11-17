import time

import scrapy
from scrapy.selector import Selector

from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class EPLSpider(scrapy.Spider):
    name = "eplmatch"

    def start_requests(self):
        url = "https://www.premierleague.com/results"
        yield SeleniumRequest(
            url=url,
            callback=self.parse,
        )
    
    def __init__(self):
        self.driver = webdriver.Chrome("E:\\HUST\\20221 Data Science\\Project\\ds-epl-matches\\scrapers\\chromedriver.exe")
        self.wait = WebDriverWait(self.driver, 20)
        self.BASE_URL = "https://www.premierleague.com/match/"
    
    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)
        
        # scroll to the end of the page -> load all matches
        new_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(20)
            prev_height = new_height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == prev_height:
                break
        
        # wait the div.loader detached off DOM
        loader_element = self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '#mainContent > div.tabbedContent > div.wrapper.col-12.tabLoader.active > div:nth-child(3) > section > div.loader')))

        '''
        page = "epl"
        filename = f'test-{page}.html'
        with open(filename, 'w') as f:
            f.write(self.driver.page_source)
        self.log(f'Saved file {filename}')
        '''

        fixtures = self.driver.find_elements(By.XPATH, '//*[@id="mainContent"]/div[3]/div[1]/div[2]/section/div[@class="fixtures__matches-list"]')
        matches = fixtures.find_elements(By.XPATH, '//*[@class="matchList]/*[@class="matchFixtureContainer"]')
        for match in matches:
            yield SeleniumRequest(
                url=self.BASE_URL + match.getAttribute("data-comp-match-item"),
                callback=self.parse_match
            )
    
    def parse_match(self, response):
        pass
