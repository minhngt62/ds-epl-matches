import time
import json
import os
from pathlib import Path
SCRAPERS_ROOT = Path(__file__).parent.parent.parent.resolve()

import scrapy

from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--window-size=1280,720")

from ..items import *


class FPLSpider(scrapy.Spider):
    name = "fplbot"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapers.pipelines.JsonWriter': 100
        }
    }

    def start_requests(self):
        url = "https://fantasy.premierleague.com/statistics"
        yield SeleniumRequest(
            url=url,
            callback=self.parse,
        )

    def __init__(
        self, timeout=10
        ):
        self.timeout = timeout
        self.savepoint = 'fplbot.jsonl'
    
    def parse(self, response):
        driver = webdriver.Chrome(
                os.path.join(SCRAPERS_ROOT, "chromedriver.exe"), 
                chrome_options=chrome_options)
        wait = WebDriverWait(driver, self.timeout)

        driver.get(response.url)
        time.sleep(5)

        # accept cookie request
        cookie_locator = 'body > div.tcf-cmp._1Qu7MokjMuBXLOM2oKVLhZ._3_H6MsAd1grAO7T3v2WdhQ > div > div > div._1QkG3L-zAijqYlFASTvCtT > div._24Il51SkQ29P1pCkJOUO-7 > button._2hTJ5th4dIYlveipSEMYHH.BfdVlAo_cgSVjDUegen0F.js-accept-all-close'
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, cookie_locator)))
        driver.find_element(By.CSS_SELECTOR, cookie_locator).click()

        # extract player table
        player_comps = driver.find_elements(By.CSS_SELECTOR, '#root > div:nth-child(2) > div > div.Layout__Main-eg6k6r-1.wXYnc > table > tbody > tr.ElementTable__ElementRow-sc-1v08od9-3 kGMjuJ')
        for player_comp in player_comps:
            # open player dialog
            driver.execute_script("arguments[0].scrollIntoView(true);", player_comp)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'td:nth-child(2) > button'))).click()

            # scrape this season
            


            
