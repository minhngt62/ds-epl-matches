# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class Player(Item):
    name = Field()
    id = Field()
    season = Field()

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.fields['defence_clean sheets'] = Field(default='0')
        self.fields['defence_goals conceded'] = Field(default='0')
        self.fields['defence_tackles'] = Field(default='0')
        self.fields['defence_tackle success %'] = Field(default='0')
        self.fields['defence_last man tackles'] = Field(default='0')
        self.fields['defence_blocked shots'] = Field(default='0')
        self.fields['defence_interceptions'] = Field(default='0')
        self.fields['defence_clearances'] = Field(default='0')
        self.fields['defence_headed clearance'] = Field(default='0')
        self.fields['defence_clearances off line'] = Field(default='0')
        self.fields['defence_recoveries'] = Field(default='0')
        self.fields['defence_duels won'] = Field(default='0')
        self.fields['defence_duels lost'] = Field(default='0')
        self.fields['defence_successful 50/50s'] = Field(default='0')
        self.fields['defence_aerial battles won'] = Field(default='0')
        self.fields['defence_aerial battles lost'] = Field(default='0')
        self.fields['defence_own goals'] = Field(default='0')
        self.fields['defence_errors leading to goal'] = Field(default='0')
        
        self.fields['teamplay_goals'] = Field(default='0') # similar to attack, but for gk ?
        self.fields['teamplay_assists'] = Field(default='0')
        self.fields['teamplay_passes'] = Field(default='0')
        self.fields['teamplay_passes per match'] = Field(default='0')
        self.fields['teamplay_big chances created'] = Field(default='0')
        self.fields['teamplay_crosses'] = Field(default='0')
        self.fields['teamplay_cross accuracy %'] = Field(default='0')
        self.fields['teamplay_through balls'] = Field(default='0')
        self.fields['teamplay_accurate long balls'] = Field(default='0')

        self.fields['discipline_yellow cards'] = Field(default='0')
        self.fields['discipline_red cards'] = Field(default='0')
        self.fields['discipline_fouls'] = Field(default='0')
        self.fields['discipline_offsides'] = Field(default='0')

        self.fields['attack_goals'] = Field(default='0')
        self.fields['attack_goals per match'] = Field(default='0')
        self.fields['attack_headed goals'] = Field(default='0')
        self.fields['attack_goals with right foot'] = Field(default='0')
        self.fields['attack_goals with left foot'] = Field(default='0')
        self.fields['attack_penalties scored'] = Field(default='0')
        self.fields['attack_freekicks scored'] = Field(default='0')
        self.fields['attack_shots'] = Field(default='0')
        self.fields['attack_shots on target'] = Field(default='0')
        self.fields['attack_shooting accuracy %'] = Field(default='0%')
        self.fields['attack_hit woodwork'] = Field(default='0')
        self.fields['attack_big chances missed'] = Field(default='0')

        self.fields['goalkeeping_saves'] = Field(default='0')
        self.fields['goalkeeping_penalties saved'] = Field(default='0')
        self.fields['goalkeeping_punches'] = Field(default='0')
        self.fields['goalkeeping_high claims'] = Field(default='0')
        self.fields['goalkeeping_catches'] = Field(default='0')
        self.fields['goalkeeping_sweeper clearances'] = Field(default='0')
        self.fields['goalkeeping_throw outs'] = Field(default='0')
        self.fields['goalkeeping_goal kicks'] = Field(default='0')

        for field in self.fields:
            self.setdefault(field, "0")

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

