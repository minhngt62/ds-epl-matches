# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class Player(Item):
    name = Field(serializer=str)
    id = Field(serializer=int)

class LineUp(Item):
    gk = Field(serializer=list)
    df = Field(serializer=list)
    mf = Field(serializer=list)
    fw = Field(serializer=list)

class Team(Item):
    name = Field(serializer=str)
    lineup = Field(serializer=LineUp)

class Match(Item):
    home_result = Field(serializer=str)
    home_team = Field(serializer=Team)
    away_team = Field(serializer=Team)

