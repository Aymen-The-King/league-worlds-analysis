import pandas as pd
from itertools import combinations
from ranking import calculate_ranking
from utils import check_repeat_matchup






def simulate_round_all(df, round_num):
    previous_rounds_df = df[df["Round"] < f"Round {round_num}"]
    ranking_df = calculate_ranking(df, round_num - 1)
    # Exclude teams with 3 wins or losses
    ranking_df = ranking_df[(ranking_df["Wins"] < 3) & (ranking_df["Losses"] < 3)]
    groups_by_wins = ranking_df.groupby("Wins")["Team"].apply(list).to_dict()
    matchups = []
    for teams in groups_by_wins.values():
        matchups.extend(list(combinations(teams, 2)))
    matchups_df = pd.DataFrame(matchups, columns=["T1", "T2"])
    matchups_df["Score T1"] = 0
    matchups_df["Score T2"] = 0
    matchups_df["Round"] = f"Round {round_num}"
    repeat_columns = []
    for index,row in matchups_df.iterrows():
        repeat_columns.append(check_repeat_matchup(df,row.loc["T1"],row.loc["T2"]))
    matchups_df["Repeat"]=repeat_columns
    return matchups_df

def add_match_result(df, t1, t2, score_t1, score_t2, round_num):
    new_row = {
        'T1': t1,
        'T2': t2,
        'Score T1': score_t1,
        'Score T2': score_t2,
        'Round': round_num
    }
    if check_repeat_matchup(df, t1, t2):
        df.loc[(df['T1'] == t1) & (df['T2'] == t2), ['Score T1', 'Score T2']] = [score_t1, score_t2]
    else:
        df = df.append(new_row, ignore_index=True)
    return df

def team_potential_draw(df, team):
    df_temp = pd.concat([df[df["T1"] == team], df[df["T2"] == team]])
    return df_temp
