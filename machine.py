import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from data_filter import team_name_change


def winner_prediction(training_data, test_data):
    """
    Filter the columns unnecessary and change the string values to integers.
    Have FTR column as label and train the model
    (RandomForestClassifier) with training_data file.
    With the model, predict the future matches.
    """
    df_train = pd.read_csv(training_data)
    df_test = pd.read_csv(test_data)

    df_train = df_train.drop(['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG',
                              'HTHG', 'HTAG', 'HST', 'AST'], axis=1)
    df_train = df_train.dropna()
    df_test = df_test.drop(['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG',
                            'HTHG', 'HTAG',  'HST', 'AST'], axis=1)
    df_test = df_test.dropna()

    # change categorical string value to int
    factor = pd.factorize(df_train['FTR'])
    df_train.FTR = factor[0]
    # definitions = factor[1]

    factor = pd.factorize(df_test['FTR'])
    df_test.FTR = factor[0]
    # definitions = factor[1]

    # split features and labels for training and test
    features_train = df_train.loc[:, df_train.columns != 'FTR']
    labels_train = df_train['FTR']
    features_test = df_test.loc[:, df_test.columns != 'FTR']
    labels_test = df_test['FTR']

    # read data for prediction
    future = pd.read_csv('season_21.csv')
    future = future[future['FTR'].isnull() == True]
    # copy data for later to save column for predicted values
    future_with_pred = future.copy()
    # drop unnecessary columns for prediction
    future = future[['HTOverall', 'ATOverall', 'all_time_win_ratio',
                     'headtohead_win_ratio', 'opp_win_ratio']]

    # ________________ Machine Learning: RandomForest

    # classifier = RandomForestClassifier(n_estimators=500,
    #                                     max_depth=10, random_state=0)

    # from sklearn.model_selection import cross_val_score
    # all_accuracies = cross_val_score(estimator=classifier, X=features_train,
    #                                  y=labels_train, cv=5)
    # print(all_accuracies)
    # print(all_accuracies.mean())

    scaler = StandardScaler()
    features_train = scaler.fit_transform(features_train)
    features_test = scaler.transform(features_test)
    future = scaler.transform(future)

    # train the model
    model = RandomForestClassifier(n_estimators=500, max_depth=15,
                                   random_state=0)
    model.fit(features_train, labels_train)

    # access the model
    train_pred = model.predict(features_train)
    train_acc = accuracy_score(labels_train, train_pred)

    test_pred = model.predict(features_test)
    test_acc = accuracy_score(labels_test, test_pred)

    future_pred = model.predict(future)
    print("The accuracy scores are", train_acc, test_acc)
    print(future_pred)

    # add prediction column for predicted value and change it to string value
    future_with_pred['Prediction'] = future_pred
    future_with_pred.loc[(future_with_pred.Prediction == 0),
                         'Prediction'] = 'L'
    future_with_pred.loc[(future_with_pred.Prediction == 1),
                         'Prediction'] = 'W'
    future_with_pred.loc[(future_with_pred.Prediction == 2),
                         'Prediction'] = 'D'

    # export as csv file
    future_with_pred.to_csv('Prediction.csv', index=False)


def point_calculation(file_name, standing_file):
    """
    Based on the future match prediction, calculate potential game points
    each team will achieve. 3 points for win, 1 points for draw,
    0 points for lose. Add the predicted points to current points.
    Sort by points and
    top team of the list is predicted champion of the league.
    """
    data = pd.read_csv(file_name)
    team_name_change(standing_file)
    standing = pd.read_csv(standing_file)

    # drop unnecessary columns
    data = data[['Date', 'HomeTeam', 'AwayTeam', 'Prediction']]
    standing = standing[['Team', 'PTS']]

    # create list of teams and dict to save points after score
    team_list = list(data['HomeTeam'].unique())
    total_point = {}

    # loop to find each team and add points based on the prediction
    for team in team_list:
        each_team = data.loc[data['HomeTeam'] == team]
        points = len(each_team[each_team['Prediction'] == 'W']) * 3 + \
            len(each_team[each_team['Prediction'] == 'D'])
        total_point[team] = points

    # loop to add points to current points
    for team, point in total_point.items():
        standing.loc[(standing['Team'] == team), 'PTS'] += point

    # sort by points and top team of the list is
    # predicted champion of the league
    standing = standing.sort_values(by='PTS', ascending=False)
    print(standing)
    return standing
