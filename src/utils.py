def check_repeat_matchup(df, team1, team2):
    condition_1 = (df['T1'] == team1) & (df['T2'] == team2)
    condition_2 = (df['T1'] == team2) & (df['T2'] == team1)
    return df[condition_1 | condition_2].shape[0] > 0

def format_ranking(df):
    def highlight(row):
        if row['Wins'] >= 3:
            return ['background-color: green'] * len(row)
        elif row['Losses'] >= 3:
            return ['background-color: red'] * len(row)
        else:
            return [''] * len(row)
    return df.style.apply(highlight, axis=1)

