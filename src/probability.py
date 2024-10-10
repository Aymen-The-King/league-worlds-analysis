from itertools import product


regions = {
    "EU": ["G2 Esports", "Fnatic", "MAD Lions"],
    "NA": ["Team Liquid", "FlyQuest"],
    "KR": ["T1", "Dplus KIA", "Hanwha Life Esports"],
    "CN": ["Weibo Gaming", "Top Esports", "BLG"],
    "TW": ["PSG Talon"]
}
region_list = ["EU", "NA", "KR", "CN", "TW"]
UpperBracket=["Top Esports","T1","Dplus KIA","Hanwha Life Esports","FlyQuest","G2 Esports"]
LowerBracket=["BLG","MAD Lions","Weibo Gaming","Fnatic","Team Liquid","PSG Talon"]
results = {region: [] for region in region_list}


def generate_matchings(teams):
    if len(teams) < 2:
        return []
    elif len(teams) == 2:
        return [[(teams[0], teams[1])]]
    else:
        matchings = []
        first_team = teams[0]
        for i in range(1, len(teams)):
            pair = (first_team, teams[i])
            remaining_teams = teams[1:i] + teams[i+1:]
            for rest in generate_matchings(remaining_teams):
                matchings.append([pair] + rest)
        return matchings
    
def remove_scenario_repeat(df,matchings):    
    index_to_remove=[]
    exist=False
    for i in range(len(matchings)) :
        for j in range(len(matchings[i])):
            if check_repeat_matchup(df,matchings[i][j][0],matchings[i][j][1])  :
                exist=True
        if exist==True :
            index_to_remove.append(i)
        exist=False    
    L_reduced = [element for idx, element in enumerate(matchings) if idx not in index_to_remove]
  
    return L_reduced


def calculate_round5_probabilities(upper_bracket_matchings,lower_bracket_matchings,region_list):

    total_scenarios = 0

    for upper_matchups in upper_bracket_matchings:
        for lower_matchups in lower_bracket_matchings:
            # Combine matchups
            round4_matchups = upper_matchups + lower_matchups
            
            # Generate all possible outcomes for Round 4
            outcomes_round4 = list(product([0, 1], repeat=6))  # 6 matches in total
            
            for outcome4 in outcomes_round4:
                # Determine Round 4 winners and losers
                round4_winners = []
                round4_losers = []
                eliminated = []
                
                for idx, result in enumerate(outcome4):
                    team1, team2 = round4_matchups[idx]
                    if idx < 3:  # Upper Bracket
                        if result == 1:
                            round4_winners.append(team1)
                            round4_losers.append(team2)
                        else:
                            round4_winners.append(team2)
                            round4_losers.append(team1)
                    else:  # Lower Bracket
                        if result == 1:
                            round4_winners.append(team1)
                            eliminated.append(team2)
                        else:
                            round4_winners.append(team2)
                            eliminated.append(team1)
                
                # Generate Round 5 matchups: Losers of Upper Bracket vs Winners of Lower Bracket
                # Need to generate all possible matchings between these teams, considering no repeats and rules
                # Since there are 3 Upper Losers and 3 Lower Winners, possible matchings are:
                # Number of matchings: 15
                
                # For simplicity, we'll assume the matchups are fixed in the order of lists
                round5_matchups = list(zip(round4_losers, round4_winners[3:]))
                
                # Generate all possible outcomes for Round 5
                outcomes_round5 = list(product([0, 1], repeat=3))
                
                for outcome5 in outcomes_round5:
                    total_scenarios += 1
                    advanced_teams = round4_winners[:3]  # Upper Bracket winners
                    eliminated_teams = eliminated.copy()
                    
                    # Simulate Round 5 matches
                    for idx, result in enumerate(outcome5):
                        team1, team2 = round5_matchups[idx]
                        if result == 1:
                            advanced_teams.append(team1)
                            eliminated_teams.append(team2)
                        else:
                            advanced_teams.append(team2)
                            eliminated_teams.append(team1)
                    
                    # Tally the number of teams from each region that advance
                    region_counts = {region: 0 for region in region_list}
                    for team in advanced_teams:
                        for region, teams in regions.items():
                            if team in teams:
                                region_counts[region] += 1
                    
                    # Append the counts to the results
                    for region in region_list:
                        results[region].append(region_counts[region])
    probabilities = {}

    for region in region_list:
        counts = results[region]
        total = len(counts)
        freq = pd.Series(counts).value_counts().sort_index()
        prob = (freq / total).reset_index()
        prob.columns = ['Teams_Advancing', 'Probability']
        probabilities[region] = prob
    return probabilities