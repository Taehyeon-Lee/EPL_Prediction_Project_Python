from data_filter import (top_scorer, team_name_change, aggregate,
                         headtohead_ratio, all_time_win_ratio, season_21)
from beautiful_soup import (scrap_overall, scrap_top_scorer, scrap_standing)
from graph import (data_for_graphs, score_prediction_graph,
                   shot_on_target_graph, contribution_graph)
from machine import winner_prediction, point_calculation


def main():
    # 1
    list_of_seasons = ['2013-14.csv', '2014-15.csv', '2015-16.csv',
                       '2016-17.csv', '2017-18.csv', '2018-19.csv',
                       '2019-20.csv', '2020-21.csv']
    list_of_overall = ['fifa14', 'fifa15', 'fifa16', 'fifa17',
                       'fifa18', 'fifa19', 'fifa20', 'fifa21']
    for i in list_of_overall:
        if i == 'fifa21':
            scrap_overall("https://www.fifaindex.com/teams/" +
                          "?league=13&order=desc", i + ".csv")
        else:
            scrap_overall("https://www.fifaindex.com/teams/" +
                          i + "/?league=13&order=desc", i + ".csv")
    scrap_top_scorer("https://www.msn.com/en-us/sports/soccer/" +
                     "premier-league/player-stats/sp-s-gs", 'top_scorers.csv')
    scrap_standing("https://www.msn.com/en-us/sports/soccer/" +
                   "premier-league/standings", "team_standing.csv")
    # 2
    top_scorer("top_scorers.csv", "team_standing.csv")
    for i in list_of_overall:
        team_name_change(i + ".csv")
    aggregate(list_of_seasons, list_of_overall, "total_matches.csv")
    headtohead_ratio("total_matches.csv")
    all_time_win_ratio("total_matches.csv")

    # 3
    data_for_graphs("top_100_scorers.csv")
    score_prediction_graph("top_100_scorers.csv")
    shot_on_target_graph("top_100_scorers.csv")
    contribution_graph("top_100_scorers.csv")

    # 4
    season_21('future_games.csv', '2020-21.csv')

    # Creating training dataset
    # name_change(list_of_overall)
    aggregate(list_of_seasons[:7], list_of_overall[:7], 'train_dataset.csv')
    all_time_win_ratio('train_dataset.csv')
    headtohead_ratio('train_dataset.csv')

    # Creating test dataset
    fifa21 = ['fifa21']
    season = ['2020-21.csv']
    # name_change(fifa21)
    aggregate(season, fifa21, 'test_dataset.csv')
    all_time_win_ratio('test_dataset.csv')
    headtohead_ratio('test_dataset.csv')

    # prepare prediction
    all_time_win_ratio('season_21.csv')
    headtohead_ratio('season_21.csv')

    winner_prediction('train_dataset.csv', 'test_dataset.csv')
    point_calculation('Prediction.csv', 'team_standing.csv')


if __name__ == '__main__':
    main()
