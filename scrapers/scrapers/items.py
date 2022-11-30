# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class Player(Item):
    name = Field(serializer=str)
    id = Field(serializer=int)
    season = Field(serializer=str)
    INDICES = ('pts', 'mp', 'gs', 'a', 'cs', 'gc', 'og', 'ps', 'pm', 'yc', 'rc', 's', 'b', 'bps', 'i', 'c', 't', 'ii')
    
    pts = Field(serializer=float)
    mp = Field(serializer=float)
    gs = Field(serializer=float)
    a = Field(serializer=float)
    cs = Field(serializer=float)
    gc = Field(serializer=float)
    og = Field(serializer=float)
    ps = Field(serializer=float)
    pm = Field(serializer=float)
    yc = Field(serializer=float)
    rc = Field(serializer=float)
    s = Field(serializer=float)
    b = Field(serializer=float)
    bps = Field(serializer=float)

    i = Field(serializer=float)
    c = Field(serializer=float)
    t = Field(serializer=float)
    ii = Field(serializer=float)

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
    season = Field(serializer=str)

