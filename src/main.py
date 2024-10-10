import pandas as pd
from data_processing import load_data
from ranking import calculate_ranking
from simulation import simulate_round_all, add_match_result
from utils import format_ranking

def main():
    # Load data
    df = load_data('data/matches.csv')
    # Calculate rankings
    ranking_df = calculate_ranking(df, round_num=1)
    print(ranking_df)
    # Simulate next round
    matchups_df = simulate_round_all(df, round_num=2)
    print(matchups_df)
    # Add a match result as an example
    df = add_match_result(df, 'Team A', 'Team B', 1, 0, 'Round 2')
    # Format and display rankings
    formatted_ranking = format_ranking(ranking_df)
    print(formatted_ranking)
    
if __name__ == "__main__":
    main()
