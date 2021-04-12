import pandas as pd
import numpy as np


def top_scorer(file_name_1, file_name_2):
    """
    Merge two datasets (top scorer dataset and current team standing dataset)
    and filter out columns unnecessary. Save top 100 scorers in the league
    """
    # read standing and top scorer csv file
    top_scorer = pd.read_csv(file_name_1)
    standing = pd.read_csv(file_name_2)
    # drop unnecessary columns
    top_scorer = top_scorer[['Rank', 'Player', 'Team', 'Game Played',
                             'Minutes Played', 'Goals', 'Shots', 'SOG']]
    standing = standing[['Team', 'Game Played', 'Team Goals']]
    # change duplicate column name
    standing = standing.rename(columns={'Game Played': 'Rounds Played'})
    # get top 100 from top scorer
    top_100_scorer = top_scorer.loc[0:99, :]
    # merge top100 scorer and standing by team
    top_scorer_final = top_100_scorer.merge(standing, left_on='Team',
                                            right_on='Team')
    top_scorer_final = top_scorer_final.sort_values(by='Rank')

    top_scorer_final.to_csv('top_100_scorers.csv', index=False)


def team_name_change(file_name):
    """
    Read a file and change team names in the file
    to unify names with other datasets
    """
    # Unify team names in files
    data = pd.read_csv(file_name)
    data = data.replace(['Manchester United' or 'Man Utd'], 'Man United')
    data = data.replace(['Manchester City'], 'Man City')
    data = data.replace(['Tottenham Hotspur' or 'Spurs'], 'Tottenham')
    data = data.replace(['Bolton Wanderers'], 'Bolton')
    data = data.replace(['Blackburn Rovers'], 'Blackburn')
    data = data.replace(['West Ham United'], 'West Ham')
    data = data.replace(['Stoke City'], 'Stoke')
    data = data.replace(['Newcastle United'], 'Newcastle')
    data = data.replace(['Wolverhampton Wanderers'], 'Wolves')
    data = data.replace(['West Bromwich Albion'], 'West Brom')
    data = data.replace(['Wigan Athletic'], 'Wigan')
    data = data.replace(['Queens Park Rangers'], 'QPR')
    data = data.replace(['Swansea City'], 'Swansea')
    data = data.replace(['Norwich City'], 'Norwich')
    data = data.replace(['Hull City'], 'Hull')
    data = data.replace(['Cardiff City'], 'Cardiff')
    data = data.replace(['Leicester City'], 'Leicester')
    data = data.replace(['Brighton & Hove Albion' or
                         'Brighton and Hove Albion'], 'Brighton')
    data = data.replace(['Hull City'], 'Hull')
    data = data.replace(['Huddersfield Town'], 'Huddersfield')
    data = data.replace(['AFC Bournemouth'], 'Bournemouth')
    data = data.replace(['Leeds United'], 'Leeds')
    data = data.replace(['Sheffield Utd' or 'Sheffield United'], 'Sheffield')
    data.to_csv(file_name, index=False)


# testing for aggregate function
def aggregate(csv_list, overall_list, csv_file_name):
    """
    Read match history datasets and team overall rating datasets,
    add overall ratings corresponding to team names
    """
    aggregated_data = []
    for i in range(len(csv_list)):
        season = csv_list[i]
        overall = overall_list[i]
        season_data = pd.read_csv(season)
        overall_data = pd.read_csv(overall + ".csv")

        season_data = season_data.merge(overall_data, left_on='HomeTeam',
                                        right_on='Team')
        season_data = season_data.rename(columns={'Overall': 'HTOverall'})
        season_data = season_data.merge(overall_data, left_on='AwayTeam',
                                        right_on='Team')
        season_data = season_data.rename(columns={'Overall': 'ATOverall'})

        cleaned = season_data[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG',
                               'FTR', 'HTHG', 'HTAG', 'HST', 'AST',
                               'HTOverall', 'ATOverall']]

        aggregated_data.append(cleaned)
        merged = pd.concat(aggregated_data)
    merged = merged.dropna()
    merged.to_csv(csv_file_name, index=False)


def headtohead_ratio(file_name):
    """
    Read a file and calculate head-to-head win ratio
    for more precise prediction
    """
    data = pd.read_csv(file_name)
    team_list = list(data['HomeTeam'].unique())
    team_data = []
    for team in team_list:
        team_matches = data[data['HomeTeam'] == team]
        headtohead = {}
        away_teams = data['AwayTeam'].unique()
        for away in away_teams:
            total_matches = data.loc[(data['AwayTeam'] == away)]
            matches_won = data.loc[(data['AwayTeam'] == away) &
                                   (data['FTR'] == 'H')]
            number_of_wins = len(matches_won)
            number_of_matches = len(total_matches)
            win_ratio = number_of_wins / number_of_matches
            headtohead[away] = win_ratio
        team_matches['headtohead_win_ratio'] = \
            team_matches['AwayTeam'].map(headtohead)
        team_data.append(team_matches)
    data = pd.concat(team_data, ignore_index=False)
    data.to_csv(file_name, index=False)


def all_time_win_ratio(file_name):
    """
    Read a file and calculate all time win ratio for more precise prediction
    """
    data = pd.read_csv(file_name)
    team_list = list(data['HomeTeam'].unique())
    all_time_ratio = {}
    for team in team_list:
        all_games = data.loc[data['HomeTeam'] == team]
        win_ratio = len(all_games[all_games['FTR'] == 'H']) / len(all_games)
        all_time_ratio[team] = win_ratio
    data['all_time_win_ratio'] = data['HomeTeam'].map(all_time_ratio)
    data['opp_win_ratio'] = data['AwayTeam'].map(all_time_ratio)
    data.to_csv(file_name, index=False)


def season_21(file_name_1, file_name_2):
    """
    Read a file with match history for 2020-21 season and a file with future
    match schedule, and combine the files and filter columns unnecessary
    and add needed columns
    """
    # unify teams' names using team_name_change function
    file_list = [file_name_1, file_name_2]
    for filename in file_list:
        team_name_change(filename)

    # get the future match data from dataset
    future = pd.read_csv(file_name_1)
    future = future[future['Result'].isnull() == True]
    # filter out unncessary columns and unify column names with the other file
    future = future[['Date', 'Home Team', 'Away Team']]
    future = future.rename(columns={"Home Team": "HomeTeam",
                                    "Away Team": "AwayTeam"})
    # add columns to match up with the other file
    future['FTHG'] = np.nan
    future['FTAG'] = np.nan
    future['FTR'] = np.nan
    future['HTHG'] = np.nan
    future['HTAG'] = np.nan
    future['HST'] = np.nan
    future['AST'] = np.nan
    # read the season 20-21 data and filter out unnecessary columns
    finished = pd.read_csv(file_name_2)
    finished = finished[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG',
                         'FTR', 'HTHG', 'HTAG', 'HST', 'AST']]
    # merge the future match data file and previous match data file
    merged = pd.concat([finished, future], ignore_index=True)

    # add hometeam overall column and awayteam overall column
    # with season 21 overall file
    overall_data = pd.read_csv('fifa21.csv')
    merged = merged.merge(overall_data, left_on='HomeTeam', right_on='Team')
    merged = merged.rename(columns={'Overall': 'HTOverall'})
    merged = merged.merge(overall_data, left_on='AwayTeam', right_on='Team')
    merged = merged.rename(columns={'Overall': 'ATOverall'})
    # remove unnecessary columns
    columns = ['Team_x', 'Team_y']
    merged = merged.drop(columns, axis=1)
    # save as 'season_21.csv' for future use
    merged.to_csv('season_21.csv', index=False)
