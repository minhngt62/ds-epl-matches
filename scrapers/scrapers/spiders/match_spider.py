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
chrome_options.add_argument("--window-size=1280,1020")

from ..items import *

class MatchSpider(scrapy.Spider):
    name = "matches"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapers.pipelines.JsonWriter': 100
        }
    }

    def start_requests(self):
        url = "https://www.premierleague.com/results"
        yield SeleniumRequest(
            url=url,
            callback=self.parse,
        )
    
    def __init__(
        self, timeout=20, 
        seasons=["2019/20"] # "2022/23", "2021/22", "2020/21", "2019/20"
        ):
        self.BASE_URL = "https://www.premierleague.com/match/"
        self.rolemap = {0: "gk", 1: "df", 2: "mf", 3: "fw"}
        self.timeout = timeout
        self.seasons = seasons
        self.output = 'matches.jsonl'

    def parse(self, response):
        # filter the season
        for season in self.seasons:
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

            # choose season
            driver.execute_script("window.scrollTo(0,0);")
            wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="mainContent"]/div[3]/div[1]/section/div[@data-dropdown-block="compSeasons"]'))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="mainContent"]/div[3]/div[1]/section/div[@data-dropdown-block="compSeasons"]/ul[@class="dropdownList"]/li[@data-option-name="{season}"]'))).click()

            # scroll to the end of the page -> load all matches
            new_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                time.sleep(3)
                prev_height = new_height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == prev_height:
                    break
            
            # wait the div.loader detached off DOM
            loader_locator = '#mainContent > div.tabbedContent > div.wrapper.col-12.tabLoader.active > div:nth-child(3) > section > div.loader'
            wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, loader_locator)))

            # find & send requests for the match page
            fixtures = driver.find_elements(By.CSS_SELECTOR, '#mainContent > div.tabbedContent > div.wrapper.col-12.tabLoader.active > div:nth-child(3) > section.fixtures > div.fixtures__matches-list')
            for fixture in fixtures:
                matches = fixture.find_elements(By.CSS_SELECTOR, 'ul.matchList > li.matchFixtureContainer')
                for match in matches:
                    yield SeleniumRequest(
                        url=self.BASE_URL + match.get_attribute("data-comp-match-item"),
                        callback=self.parse_match,
                        cb_kwargs=dict(season=season)
                    )
    
    def parse_match(self, response, season="2019/20"):
        driver = webdriver.Chrome(os.path.join(SCRAPERS_ROOT, "chromedriver.exe"))
        wait = WebDriverWait(driver, self.timeout)
        driver.get(response.url)
        time.sleep(5)

        # accept cookie request
        try:
            cookie_locator = 'body > div.tcf-cmp._1Qu7MokjMuBXLOM2oKVLhZ._3_H6MsAd1grAO7T3v2WdhQ > div > div > div._1QkG3L-zAijqYlFASTvCtT > div._24Il51SkQ29P1pCkJOUO-7 > button._2hTJ5th4dIYlveipSEMYHH.BfdVlAo_cgSVjDUegen0F.js-accept-all-close'
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, cookie_locator)))
            driver.find_element(By.CSS_SELECTOR, cookie_locator).click()
        except TimeoutError:
            pass
        
        # switch to the "Line-ups" tab
        lineup_locator = "#mainContent > div > section.mcContent > div.centralContent > div.mcTabsContainer > div.wrapper.col-12 > div > div > ul > li.matchCentreSquadLabelContainer"
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, lineup_locator)))
        driver.find_element(By.CSS_SELECTOR, lineup_locator).click()
        time.sleep(2)

        # lineup & team
        container_locator = "#mainContent > div > section.mcContent > div.centralContent > div.mcTabsContainer > div.mcTabs > section.squads.mcMainTab.active > div.wrapper > div.matchLineups"
        container = driver.find_element(By.CSS_SELECTOR, container_locator)
        home = self.__parse_team_container(container.find_element(By.CSS_SELECTOR, "div.teamList.mcLineUpContainter.homeLineup.active"))
        away = self.__parse_team_container(container.find_element(By.CSS_SELECTOR, "div.teamList.mcLineUpContainter.awayLineup"))

        # match result
        score = driver.find_element(By.CSS_SELECTOR, "#mainContent > div > section.mcContent > div.centralContent > section > div.scoreboxContainer > div > div > div.teamsContainer > div.matchScoreContainer > div > div").text
        goals = [int(goal.strip(' "')) for goal in score.split("-")]

        yield Match(
            home_team=home,
            away_team=away,
            home_result="win" if goals[0] > goals[1] else ("draw" if goals[0] == goals[1] else "lose"),
            season=season
        )

    def __parse_team_container(self, team_container):
        positions = team_container.find_elements(By.CSS_SELECTOR, 'div > div.matchLineupTeamContainer > ul')
        lineup = LineUp()
        i = 0
        while i < 4:
            players = positions[i].find_elements(By.CSS_SELECTOR, 'li.player')
            #time.sleep(1)
            pos_field = []
            for player in players:
                pos_field.append(Player(
                    name=player.find_element(By.CSS_SELECTOR, 'a > div.info > span.name').text.replace(
                        player.find_element(By.CSS_SELECTOR, 'a > div.info > span.name > div').text, ""
                    ).strip(),
                    id=player.find_element(By.CSS_SELECTOR, 'a > img').get_attribute("data-player")
                ))
            lineup[self.rolemap[i]] = pos_field
            i += 1
        
        return Team(
            name=team_container.find_element(By.CSS_SELECTOR, "div > header.squadHeader > div.position").text.replace(
                team_container.find_element(By.CSS_SELECTOR, "div > header.squadHeader > div.position > .matchTeamFormation").text, ""
            ).strip(),
            lineup=lineup
        )

        
        
        
