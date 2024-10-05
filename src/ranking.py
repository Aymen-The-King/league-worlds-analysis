import pandas as pd

def calculate_ranking(df, round_num):
    # Filter matches up to the specified round
    filtered_df = df[df["Round"] <= f"Round {round_num}"]
    # Initialize ranking dictionary
    ranking = {}
    # Calculate wins, losses, games played
    for _, row in filtered_df.iterrows():
        t1, t2 = row['T1'], row['T2']
        score_t1, score_t2 = row['Score T1'], row['Score T2']
        for team in [t1, t2]:
            if team not in ranking:
                ranking[team] = {"Wins": 0, "Losses": 0, "Games Played": 0}
        if score_t1 > score_t2:
            ranking[t1]["Wins"] += 1
            ranking[t2]["Losses"] += 1
        else:
            ranking[t1]["Losses"] += 1
            ranking[t2]["Wins"] += 1
        ranking[t1]["Games Played"] += 1
        ranking[t2]["Games Played"] += 1
    # Convert to DataFrame
    ranking_df = pd.DataFrame.from_dict(ranking, orient='index').reset_index()
    ranking_df.columns = ["Team", "Wins", "Losses", "Games Played"]
    # Sort by Wins and Games Played
    ranking_df = ranking_df.sort_values(by=["Wins", "Games Played"], ascending=[False, True]).reset_index(drop=True)
    # Add Rank column
    ranking_df['Rank'] = ranking_df.index + 1
    return ranking_df[["Rank", "Team", "Wins", "Losses", "Games Played"]]
