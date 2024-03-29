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
chrome_options.add_argument("--window-size=1280,1200")


from ..items import *
from scrapy import Item

class PlayerSpider(scrapy.Spider):
    name = "players"
    custom_settings = {
        'ITEM_PIPELINES': {
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
        seasons: List[str] = ["2018/19", "2019/20", "2020/21", "2021/22"],
        preload: str = os.path.join(SCRAPERS_ROOT, "url_players.jsonl")
        ):
        self.seasons = seasons
        self.output = "players.jsonl"
        self.load_relay = 3
        self.preload = preload

        self.crawls: List[Dict[str, str]] = [] # {"url": url, "season": season}

    def crawl(self, response) -> None:
        if not self.preload:
            for season in self.seasons:
                driver = webdriver.Chrome(
                    os.path.join(SCRAPERS_ROOT, "chromedriver.exe"), 
                    chrome_options=chrome_options
                )
                
                driver.get(response.url)
                time.sleep(self.load_relay)

                self._accept_cookie(driver, "body > div.tcf-cmp._1Qu7MokjMuBXLOM2oKVLhZ._3_H6MsAd1grAO7T3v2WdhQ > div > div > div._1QkG3L-zAijqYlFASTvCtT > div._24Il51SkQ29P1pCkJOUO-7 > button._2hTJ5th4dIYlveipSEMYHH.BfdVlAo_cgSVjDUegen0F.js-accept-all-close")
                self._close_adv(driver, "#advertClose")
                
                driver.execute_script("window.scrollTo(0,0);")
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="mainContent"]/div[2]/div[1]/div/section/div[@data-dropdown-block="compSeasons"]'))).click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="mainContent"]/div[2]/div[1]/div/section/div[@data-dropdown-block="compSeasons"]/ul[@class="dropdownList"]/li[@data-option-name="{season}"]'))).click()

                self._scroll_to_bottom(driver)
                loader_path = '#mainContent > div.tabbedContent > div.wrapper.col-12.tabLoader.active > div:nth-child(3) > section > div.loader'
                WebDriverWait(driver, 20).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, loader_path)))

                player_containers = driver.find_elements(By.CSS_SELECTOR, "#mainContent > div.playerIndex > div.wrapper > div > div > table > tbody > tr")
                for player in player_containers:
                    #position = player.find_element(By.CSS_SELECTOR, "td:nth-child(2)")
                    url = player.find_element(By.CSS_SELECTOR, "td:nth-child(1) > a")
                    self.crawls.append(
                        {
                            "id": url.find_element(By.CSS_SELECTOR, "img").get_attribute("data-player"),
                            "url": url.get_attribute("href").lstrip("//").replace("overview", "stats"),
                            "season": season,
                            "name": url.text
                        }
                    )
            self._save_urls()
        else:
            with open(self.preload, "r") as f:
                self.crawls: List[Dict[str, str]] = json.load(f)

        for crawl in self.crawls:
            yield SeleniumRequest(
                url=crawl["url"],
                callback=self.parse,
                cb_kwargs=dict(crawl=crawl)
            )
    
    def parse(self, response, crawl) -> Player:
        driver = webdriver.Chrome(
            os.path.join(SCRAPERS_ROOT, "chromedriver.exe"), 
            chrome_options=chrome_options
        )
        
        driver.get(response.url)
        time.sleep(1)
        
        self._accept_cookie(driver, "body > div.tcf-cmp._1Qu7MokjMuBXLOM2oKVLhZ._3_H6MsAd1grAO7T3v2WdhQ > div > div > div._1QkG3L-zAijqYlFASTvCtT > div._24Il51SkQ29P1pCkJOUO-7 > button._2hTJ5th4dIYlveipSEMYHH.BfdVlAo_cgSVjDUegen0F.js-accept-all-close")
        self._close_adv(driver, "#advertClose")

        driver.execute_script("window.scrollTo(0,0);")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="mainContent"]/div[3]/div/div/div[2]/div/div/section/div[@data-dropdown-block="compSeasons"]'))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="mainContent"]/div[3]/div/div/div[2]/div/div/section/div[@data-dropdown-block="compSeasons"]/ul[@class="dropdownList"]/li[@data-option-name="{crawl["season"]}"]'))).click()
        time.sleep(self.load_relay)

        player = Player()
        player["season"] = crawl["season"]
        player["id"] = crawl["id"] 
        player["name"] = crawl["name"]

        stats_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainContent > div.wrapper.hasFixedSidebar > div > div > div.playerInfo > div > div > ul")))
        stats_blocks = stats_container.find_elements(By.CSS_SELECTOR, "li > div.statsListBlock")
        for block in stats_blocks:
            header = block.find_element(By.CSS_SELECTOR, "div.headerStat").text.strip().lower().replace(" ", "")
            stats = block.find_elements(By.CSS_SELECTOR, "div.normalStat > span.stat")
            for stat in stats:
                level = stat.find_element(By.CSS_SELECTOR, "span").text
                perf = stat.text.strip(f" {level}").strip().lower()
                player[f"{header}_{perf}"] = level.strip(" %")
        
        yield player


    def _save_urls(self) -> None:
        with open(os.path.join(SCRAPERS_ROOT, "url_" + self.output), "w") as f:
            json.dump(self.crawls, f)
            
    def _accept_cookie(self, driver: webdriver.Chrome, path):
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, path))).click()
        except:
            pass

    def _close_adv(self, driver: webdriver.Chrome, path):
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, path))).click()
        except:
            pass
    
    def _scroll_to_bottom(self, driver: webdriver.Chrome):
        new_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(self.load_relay)
            prev_height = new_height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == prev_height:
                break