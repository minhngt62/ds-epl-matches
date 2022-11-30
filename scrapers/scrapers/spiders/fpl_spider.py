import time
import json
import os
from pathlib import Path
SCRAPERS_ROOT = Path(__file__).parent.parent.parent.resolve()

import scrapy

from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions as SE
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--window-size=1280,1020")

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
        self, timeout=10, this_season='2022/23'
        ):
        self.cur_ss = this_season
        self.timeout = timeout
        self.savepoint = 'fplbot.jsonl'
    
    def parse(self, response):
        driver = webdriver.Chrome(
                os.path.join(SCRAPERS_ROOT, "chromedriver.exe"), 
                chrome_options=chrome_options)
        wait = WebDriverWait(driver, self.timeout)
        action = ActionChains(driver)

        driver.get(response.url)
        time.sleep(5)

        # accept cookie request
        cookie_locator = 'body > div.tcf-cmp._1Qu7MokjMuBXLOM2oKVLhZ._3_H6MsAd1grAO7T3v2WdhQ > div > div > div._1QkG3L-zAijqYlFASTvCtT > div._24Il51SkQ29P1pCkJOUO-7 > button._2hTJ5th4dIYlveipSEMYHH.BfdVlAo_cgSVjDUegen0F.js-accept-all-close'
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, cookie_locator)))
        driver.find_element(By.CSS_SELECTOR, cookie_locator).click()
        
        # extract player table
        while True:
            player_cps = driver.find_elements(By.CSS_SELECTOR, '#root > div:nth-child(2) > div > div.Layout__Main-eg6k6r-1.wXYnc > table > tbody > tr.ElementTable__ElementRow-sc-1v08od9-3.kGMjuJ')
            for player_cp in player_cps:
                # open player dialog
                #driver.execute_script("arguments[0].scrollIntoView(true);", player_cp)
                action.move_to_element(wait.until(EC.element_to_be_clickable(player_cp.find_element(By.CSS_SELECTOR, 'td:nth-child(2) > button')))).click().perform()
                
                # player info
                name = driver.find_element(By.CSS_SELECTOR, '#root-dialog > div > dialog > div > div.Dialog__StyledDialogBody-sc-5bogmv-9.jyKAwP.ism-overflow-scroll > div.ElementDialog__Summary-gmefnd-1.evNMwj > div.sc-bdnxRM.sc-gtsrHT.dDFKXk.gfuSqG > div:nth-child(2) > h2.ElementDialog__ElementHeading-gmefnd-3.fcMozp').text
                id = driver.find_element(By.CSS_SELECTOR, '#root-dialog > div > dialog > div > div.Dialog__StyledDialogBody-sc-5bogmv-9.jyKAwP.ism-overflow-scroll > div.ElementDialog__Summary-gmefnd-1.evNMwj > div.sc-bdnxRM.sc-gtsrHT.dDFKXk.gfuSqG > div.sc-bdnxRM.hpgALm > img').get_attribute('src')

                # scrape this season
                totals_cp = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#root-dialog > div > dialog > div > div.Dialog__StyledDialogBody-sc-5bogmv-9.jyKAwP.ism-overflow-scroll > div:nth-last-child(2) > div > div.sc-bdnxRM.hVwLXd > div > table > tfoot')))
                ix_cps = totals_cp.find_elements(By.CSS_SELECTOR, 'tr > td')[:18] # first 18 indices
                yield Player(
                    {'name': name} | # .replace("\n", " ")
                    {'id': id, "season": self.cur_ss} | # .split("/")[-1].split(".")[0]
                    {Player.INDICES[i]: float(ix_cps[i].text) for i in range(len(ix_cps))}
                )

                # scrape previous seasons
                try:
                    table_cps = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#root-dialog > div > dialog > div > div.Dialog__StyledDialogBody-sc-5bogmv-9.jyKAwP.ism-overflow-scroll > div:nth-child(2) > div > div.sc-bdnxRM.cxwWgD > div.ElementDialog__ScrollTable-gmefnd-16.lkCaAQ > table > tbody')))
                    pre_ss_cps = table_cps.find_elements(By.CSS_SELECTOR, 'tr')
                    for pre_ss_cp in pre_ss_cps:
                        ix_cells = pre_ss_cp.find_elements(By.CSS_SELECTOR, 'td')[:19]
                        yield Player(
                            {'name': name} | 
                            {'id': id, "season": ix_cells[0].text} |
                            {Player.INDICES[i-1]: float(ix_cells[i].text) for i in range(1, len(ix_cps))}
                        )
                except SE.TimeoutException:
                    pass
                
                # exit dialog
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root-dialog > div > dialog > div > div:nth-child(1) > div > button'))).click()
        
            # next page (if can't, assume scraper done)
            try:
                action.move_to_element(wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div:nth-child(2) > div > div.Layout__Main-eg6k6r-1.wXYnc > div.sc-bdnxRM.sc-gtsrHT.eVZJvz.gfuSqG > button:nth-child(4)')))).click().perform()
                time.sleep(2)
            except:
                break
