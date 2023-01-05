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
        self.fields['defence_clean sheats'] = Field()
        self.fields['defence_goals conceded'] = Field()
        self.fields['defence_tackles'] = Field()
        self.fields['defence_tackle sucess %'] = Field()
        self.fields['defence_last man tackles'] = Field()
        self.fields['defence_blocked shots'] = Field()
        self.fields['defence_interceptions'] = Field()
        self.fields['defence_clearances'] = Field()
        self.fields['defence_headed clearance'] = Field()
        self.fields['defence_clearances off line'] = Field()
        self.fields['defence_recoveries'] = Field()
        self.fields['defence_duels won'] = Field()
        self.fields['defence_duels lost'] = Field()
        self.fields['defence_successful 50/50s'] = Field()
        self.fields['defence_ariel battles won'] = Field()
        self.fields['defence_ariel battles lost'] = Field()
        self.fields['defence_own goals'] = Field()
        self.fields['defence_errors leading to goal'] = Field()
        
        self.fields['teamplay_goals'] = Field() # similar to attack, but for gk ?
        self.fields['teamplay_assists'] = Field()
        self.fields['teamplay_passes'] = Field()
        self.fields['teamplay_passes per match'] = Field()
        self.fields['teamplay_big chances created'] = Field()
        self.fields['teamplay_crosses'] = Field()
        self.fields['teamplay_cross accuracy %'] = Field()
        self.fields['teamplay_through balls'] = Field()
        self.fields['teamplay_accurate long balls'] = Field()

        self.fields['discipline_yellow cards'] = Field()
        self.fields['discipline_red cards'] = Field()
        self.fields['discipline_fouls'] = Field()
        self.fields['discipline_offsides'] = Field()

        self.fields['attack_goals'] = Field()
        self.fields['attack_goals per match'] = Field()
        self.fields['attack_headed goals'] = Field()
        self.fields['attack_goals with right foot'] = Field()
        self.fields['attack_goals with left foot'] = Field()
        self.fields['attack_penalties scored'] = Field()
        self.fields['attack_freekicks scored'] = Field()
        self.fields['attack_shots'] = Field()
        self.fields['attack_shots on target'] = Field()
        self.fields['attack_shooting accuracy %'] = Field()
        self.fields['attack_hit woodwork'] = Field()
        self.fields['attack_big chances missed'] = Field()

        self.fields['goalkeeping_saves'] = Field()
        self.fields['goalkeeping_penalties saved'] = Field()
        self.fields['goalkeeping_punches'] = Field()
        self.fields['goalkeeping_high claims'] = Field()
        self.fields['goalkeeping_catches'] = Field()
        self.fields['goalkeeping_sweeper clearances'] = Field()
        self.fields['goalkeeping_throw outs'] = Field()
        self.fields['goalkeeping_goal kicks'] = Field()

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

