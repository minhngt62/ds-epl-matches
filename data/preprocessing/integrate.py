import pandas as pd
from preprocess.features import *


def integrate(epl, players):
    all_season = players['season'].unique()
    wno_players = players.copy()

    for season in all_season:
        null_record = {'id': -1, 'season': season}
        for feat in players.columns[2:]:
            null_record[feat] = -2
        wno_players = wno_players.append(null_record, ignore_index=True)

    copy_ordered_epl = epl.copy()
    for i in range(len(all_pos)):
        copy_ordered_epl = copy_ordered_epl.merge(wno_players, how='left', left_on=[all_pos[i], 'season'],
                                                  right_on=['id', 'season'], suffixes=(f"_{i - 1}", f"_{i}"))
    re_cols = dict(zip(copy_ordered_epl.columns[-19:], players.drop(columns=['season']).columns + '_26'))
    copy_ordered_epl.rename(columns=re_cols)

    copy_ordered_epl.to_csv('final_dataset.csv', index=False)

    dropped_copy_ordered_epl = copy_ordered_epl.copy()
    dropped_copy_ordered_epl.drop(columns=dropped_copy_ordered_epl.columns[30], inplace=True)
    dropped_copy_ordered_epl.drop(columns=dropped_copy_ordered_epl.columns[:29], inplace=True)
    dropped_copy_ordered_epl.drop(columns=[col for col in dropped_copy_ordered_epl.columns if 'id' in col], inplace=True)

    dropped_copy_ordered_epl.to_csv('dropped_name_id_season_final_dataset.csv', index=False)
