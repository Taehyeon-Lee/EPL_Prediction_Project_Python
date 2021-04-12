import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


def data_for_graphs(file_name):
    """
    Calculate statistics needed for graphs and add columns to dataset.
    Change data values to integer if the value is in string.
    """
    data = pd.read_csv(file_name)

    # change column data type to integer
    data["Minutes Played"] = \
        data["Minutes Played"].str.replace(",", "").astype(int)

    # calculate minutes left for rest of the season
    total_match_min = data['Rounds Played'] * 90
    percent_playing_time = data['Minutes Played'] / total_match_min
    game_left = 38 - data['Rounds Played']
    season_min_left = game_left * 90 * percent_playing_time

    # calculate predicted goals
    data['min_per_goal'] = data['Minutes Played'] / data['Goals']
    data['min_per_shot'] = data['Minutes Played'] / data['Shots']
    data['shots_per_goal'] = data['Shots'] / data['Goals']
    data['shots_in_90_min'] = data['Shots'] / data['Minutes Played'] * 90
    data['estimate_shots'] = season_min_left / data['min_per_shot']
    data['estimate_goals'] = data['estimate_shots'] / data['shots_per_goal']
    data['predict_goals'] = data['Goals'] + data['estimate_goals']
    data['contribution_percentage'] = data['Goals'] / data['Team Goals'] * 100
    data['shots_per_goal'] = data['Shots'] / data['Goals']
    data['goal_conversion_percentage'] = 1 / data['shots_per_goal'] * 100
    data['shot_on_target_percentage'] = data['SOG'] / data['Shots'] * 100
    splitted = data['Player'].str.split()
    data['LastName'] = splitted.str[-1]
    data.to_csv(file_name)


def score_prediction_graph(file_name):
    """
    Plot score prediction based on the statistics of top 10 players
    in bar chart. The statistics include minutes played,
    shots per a game, goal conversion ratio, and else.
    Blue bars represent current goals scored
    and red bars represent predicted goals.
    """
    data = pd.read_csv(file_name)

    # graph the stacked bar plot
    sns.set_style("darkgrid", {"axes.facecolor": ".9"})
    # bottom bar will be the goals made for now
    bottom_data = data.loc[:9, ('LastName', 'Goals')]
    # top bar will be the estimated goals
    data['predict_goals'] = data['predict_goals'].astype(int)
    top_data = data.loc[:9, ('LastName', 'predict_goals')]
    plt.figure(figsize=(10, 7))
    # plot the top bar with red color
    top_plot = sns.barplot(data=top_data, x="LastName",
                           y="predict_goals", color="r")
    # present the estimated goals on the top of the bars
    for i in top_plot.patches:
        top_plot.annotate('{:.0f}'.format(i.get_height()),
                          (i.get_x()+0.4, i.get_height()),
                          ha='center', va='bottom', color='black')

    # plot the bottom bar with blue color
    bottom_plot = sns.barplot(data=bottom_data, x="LastName",
                              y="Goals", color="b")
    for j in bottom_plot.patches:
        bottom_plot.annotate('{:.0f}'.format(j.get_height()),
                             (j.get_x()+0.4, j.get_height()),
                             ha='center', va='bottom', color='black')
    # legends
    topbar = plt.Rectangle((0, 0), 1, 1, fc="red", edgecolor='none')
    bottombar = plt.Rectangle((0, 0), 1, 1, fc='#0000A3',  edgecolor='none')
    le = plt.legend([bottombar, topbar], ['Now', 'Estimate'],
                    loc=1, ncol=2, prop={'size': 10})
    le.draw_frame(False)

    # name the axis, title, and the file
    # rotate the axis in 35 degree
    plt.setp(top_plot.get_xticklabels(), rotation=35, fontsize=10)
    plt.xlabel('Top 10 Players', fontsize=15)
    plt.ylabel('Goal Scored', fontsize=15)
    plt.title('Estimated goals at the end of the season', fontsize=20)
    plt.savefig('estimated_goal.png', bbox_inches='tight')


def shot_on_target_graph(file_name):
    """
    Plot a scatter plot with goal conversion rate and shot on target rate.
    Goal converstion rate (goal per shots) are in y-axis and shot on target
    rate in x-axis. Present top 10 scorers' names in the graph to see
    their efficiencies compared to other players.
    """
    data = pd.read_csv(file_name)
    # graph the scatter plot
    sns.set(rc={'figure.figsize': (25, 20), 'axes.labelsize': 12})
    graph = sns.relplot(data=data, x='shot_on_target_percentage',
                        y='goal_conversion_percentage',
                        hue='LastName', legend=False)
    # loop and display only top 10 scorers in the graph
    for i in range(data.shape[0]-90):
        plt.text(x=data.shot_on_target_percentage[i],
                 y=data.goal_conversion_percentage[i], s=data.LastName[i],
                 fontdict=dict(color='black', size=8))

    graph.set_axis_labels('Shots on Target', 'Goal Conversion Rate')
    # Title for the complete figure
    graph.fig.suptitle('Shots on Target (%) and Goal Conversion Rate (%)',
                       fontsize='large')
    plt.savefig('efficiency.png', bbox_inches='tight')


def contribution_graph(file_name):
    """
    Plot top 10 scorers' goals and their team goals to present
    their contribution to the team. Green bar represents
    team goals and light green bar represents player's goals.
    """
    data = pd.read_csv(file_name)
    # graph the stacked bar plot
    sns.set_style("darkgrid", {"axes.facecolor": ".9"})

    # bottom bar will be the goals made for now
    bottom_data = data.loc[:9, ('LastName', 'Goals')]
    # top bar will be the estimated goals
    data['percentage'] = (data['Goals'] / data['Team Goals'] * 100).astype(int)
    top_data = data.loc[:9, ('LastName', 'Team Goals')]
    plt.figure(figsize=(10, 7))
    # plot the top bar and bottom bar
    top_plot = sns.barplot(data=top_data, x="LastName", y="Team Goals",
                           color="#2ca25f")
    bottom_plot = sns.barplot(data=bottom_data, x="LastName", y="Goals",
                              color="#99d8c9")

    # present the player goals and team goals on the bars
    for i in bottom_plot.patches:
        bottom_plot.annotate('{:.0f}'.format(i.get_height()),
                             (i.get_x()+0.4, i.get_height()),
                             ha='center', va='bottom', color='black')

    # legends
    topbar = plt.Rectangle((0, 0), 1, 1, fc="#2ca25f", edgecolor='none')
    bottombar = plt.Rectangle((0, 0), 1, 1, fc='#99d8c9',  edgecolor='none')
    le = plt.legend([bottombar, topbar], ['Player Goals', 'Team Goals'],
                    loc=1, ncol=1, prop={'size': 10})
    le.draw_frame(False)

    # name the axis, title, and the file
    # rotate the axis in 35 degree
    plt.setp(top_plot.get_xticklabels(), rotation=35)
    plt.title('Player\'s contribution to the Team', fontsize=20)
    plt.xlabel('Players vs Team', fontsize=15)
    plt.ylabel('Goal Scored', fontsize=15)
    plt.savefig('contribution.png', bbox_inches='tight')
