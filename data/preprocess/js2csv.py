import json
import pandas as pd
import numpy as np
from preprocess import *


def read_json(path):
    data = []
    with open(path) as f:
        for line in f:
            try:
                data.append(json.loads(line.strip()))
            except ValueError:
                pass
    return data


def to_df(path):
    data = read_json(path)
    list_name = list(data[0].keys())
    df = pd.DataFrame(data, columns=list_name)
    return df


def epl(path):
    df = to_df(path)
    hars = {'home/name': [], 'away/name': []}
    all_pos_home = set()
    all_pos_away = set()
    for i in range(df.shape[0]):
        hars['home/name'].append(df['home_team'].iloc[i]['name'])
        hars['away/name'].append(df['away_team'].iloc[i]['name'])
    hars['home_result'] = df['home_result']
    hars['season'] = df['season']

    for i in range(df.shape[0]):
        pos = df['home_team'].iloc[i]['lineup']
        for sub_pos, player in pos.items():
            for i in range(len(player)):
                if f'home/{sub_pos}_{i}' not in hars.keys():
                    hars[f'home/{sub_pos}_{i}'] = []
                    all_pos_home.add(f'home/{sub_pos}_{i}')
        pos = df['away_team'].iloc[i]['lineup']
        for sub_pos, player in pos.items():
            for i in range(len(player)):
                if f'away/{sub_pos}_{i}' not in hars.keys():
                    hars[f'away/{sub_pos}_{i}'] = []
                    all_pos_away.add(f'away/{sub_pos}_{i}')

    for i in range(df.shape[0]):
        pos = df['home_team'].iloc[i]['lineup']
        for sub_pos in all_pos_home:
            try:
                hars[f'{sub_pos}'].append(int(pos[sub_pos[5:-2]][int(sub_pos[-1])]["id"][1:]))
            except:
                hars[f'{sub_pos}'].append(np.nan)
        pos = df['away_team'].iloc[i]['lineup']
        for sub_pos in all_pos_away:
            try:
                hars[f'{sub_pos}'].append(int(pos[sub_pos[5:-2]][int(sub_pos[-1])]["id"][1:]))
            except:
                hars[f'{sub_pos}'].append(np.nan)

    hars = pd.DataFrame(hars)

    dataset = hars[columns]

    return dataset


def fpl(path):
    players = to_df(path)
    players = players.drop(columns=['name'], axis=1)
    ids = []
    for i in range(players.shape[0]):
        ids.append(players.iloc[i]['id'].split('/')[-1][1:-4])
    players['id'] = ids

    return players


def to_csv(func, json_path, dest):
    dataset = func(json_path)
    dataset.to_csv(dest, index=False)



