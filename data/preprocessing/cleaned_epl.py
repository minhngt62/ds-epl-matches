import pandas as pd
from preprocess.features import all_pos

def reindex_epl(epl, players):
    # load csv
    epl = pd.read_csv(epl)
    players = pd.read_csv(players)

    epl = epl.fillna(-1)
    epl[all_pos] = epl[all_pos].astype(int)
    position = ['home/gk', 'home/df', 'home/mf', 'home/fw',
                'away/gk', 'away/df', 'away/mf', 'away/fw']

    # sort epl by ict values
    ict_df = epl.copy()
    ict_players = players[['id', 'season', 'ii']]
    for i in range(len(all_pos)):
        ict_df = ict_df.merge(ict_players, how='left', left_on=[all_pos[i], 'season'], right_on=['id', 'season'],
                              suffixes=(f"_{i - 1}", f"_{i}"))
    ict_df.rename(columns={'ii': 'ii_26', 'id': 'id_26'}, inplace=True)
    ict_df.drop(columns=[id_col for id_col in ict_df.columns if 'id' in id_col], inplace=True)
    ict_df[list(ict_df.columns)[2:29]] = ict_df[list(ict_df.columns)[31:]]
    ict_df.drop(columns=list(ict_df.columns)[31:], inplace=True)

    copy_ict_df = ict_df.T.copy()
    copy_epl = epl.T.copy()
    for col in copy_ict_df.columns:
        for pos in position:
            pos_order = [row for row in copy_epl.index if pos in row]
            sorted_pos = copy_epl[col].loc[pos_order].sort_values(ascending=False, ignore_index=False,
                                                                  key=lambda x: copy_ict_df[col].loc[
                                                                      [row for row in copy_ict_df.index if
                                                                       pos in row]].astype(float))
            re_cols = dict(zip(pos_order, sorted_pos.index))
            copy_epl[col].loc[pos_order] = sorted_pos.rename(index=re_cols)

    # Sorted epl
    ordered_epl = copy_epl.T.copy()
    ordered_epl.to_csv('ordered_epl.csv', index=False)

