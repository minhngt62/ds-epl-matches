import time
import json
import os
from typing import List, Dict, Union, Any, Optional
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
chrome_options.add_argument("--window-size=1280,1020")


from ..items import *

class PlayerSpider:
    name = "playerbot"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapers.pipelines.PlayerDefaultFields': 50,
            'scrapers.pipelines.JsonWriter': 100
        }
    }

    def start_requests(self):
        url = "https://www.premierleague.com/players"
        yield SeleniumRequest(
            url=url,
            callback=self.crawl
        )

    def __init__(
        self,
        seasons: List[str] = ["2019/20", "2020/21", "2021/22"]
        ):
        self.seasons = seasons
        self.output = "players.jsonl"
        self.load_relay = 3

        self.crawls: List[Dict[str, str]] = [] # {"url": url, "season": season}

    def crawl(self, response) -> None:
        for season in self.seasons:
            driver = webdriver.Chrome(
                os.path.join(SCRAPERS_ROOT, "chromedriver.exe"), 
                chrome_options=chrome_options
            )
            
            driver.get(response.url)
            time.sleep(self.load_relay)

            cookie_path = "body > div.tcf-cmp._1Qu7MokjMuBXLOM2oKVLhZ._3_H6MsAd1grAO7T3v2WdhQ > div > div > div._1QkG3L-zAijqYlFASTvCtT > div._24Il51SkQ29P1pCkJOUO-7 > button._2hTJ5th4dIYlveipSEMYHH.BfdVlAo_cgSVjDUegen0F.js-accept-all-close"
            self._accept_cookie(cookie_path)

            driver.execute_script("window.scrollTo(0,0);")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="mainContent"]/div[3]/div[1]/section/div[@data-dropdown-block="compSeasons"]'))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="mainContent"]/div[3]/div[1]/section/div[@data-dropdown-block="compSeasons"]/ul[@class="dropdownList"]/li[@data-option-name="{season}"]'))).click()

            new_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                time.sleep(self.load_relay)
                prev_height = new_height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == prev_height:
                    break
            loader_path = '#mainContent > div.tabbedContent > div.wrapper.col-12.tabLoader.active > div:nth-child(3) > section > div.loader'
            WebDriverWait(driver, 20).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, loader_path)))

            player_containers = driver.find_elements(By.CSS_SELECTOR, "#mainContent > div.playerIndex > div.wrapper > div > div > table > tbody > tr")
            for player in player_containers:
                position = player.find_element(By.CSS_SELECTOR, "td:nth-child(2) > a")
                url = player.find_element(By.CSS_SELECTOR, "td:nth-child(1) > a")
                self.crawls.append(
                    {
                        "url": url.get_attribute("href").lstrip("//").replace("overview", "stats"),
                        "season": season,
                        "postion": position.text
                    }
                )
        
        self._save_urls()
        self._parse()
    
    def _parse(self):
        cookie_path = "body > div.tcf-cmp._1Qu7MokjMuBXLOM2oKVLhZ._3_H6MsAd1grAO7T3v2WdhQ > div > div > div._1QkG3L-zAijqYlFASTvCtT > div._24Il51SkQ29P1pCkJOUO-7 > button._2hTJ5th4dIYlveipSEMYHH.BfdVlAo_cgSVjDUegen0F.js-accept-all-close"
        for crawl in self.crawls:
            driver = webdriver.Chrome(
                os.path.join(SCRAPERS_ROOT, "chromedriver.exe"), 
                chrome_options=chrome_options
            )
            
            driver.get(crawl["url"])
            time.sleep(self.load_relay)
            
            self._accept_cookie(cookie_path)
            adclose_path = "#advertClose"
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, adclose_path))).click()

            driver.execute_script("window.scrollTo(0,0);")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="mainContent"]/div[3]/div/div/div[2]/div/div/section/div[@data-dropdown-block="compSeasons"]'))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="mainContent"]/div[3]/div/div/div[2]/div/div/section/div[@data-dropdown-block="compSeasons"]/ul[@class="dropdownList"]/li[@data-option-name="{crawl["season"]}"]'))).click()

            pass

    def _save_urls(self) -> None:
        with open("player_urls.json", "w") as f:
            json.dump(self.crawls, f)
            
    def _accept_cookie(self, driver: webdriver.Chrome, path):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, path)))
        driver.find_element(By.CSS_SELECTOR, path).click()