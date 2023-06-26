# EPL_Prediction_Project_Python
English Premier League Season 20-21  champion and top scorer prediction using Random Forest Machine Learning Algorithm

# Motivation
Even if the world of sports is a constant competition, behind the scenes, money to organize and manage a team plays a significant role. In order to get sufficient funds and a budget, the team manager should perform well in the league and come up with a winning strategy. To set up a successful plan, we believe, collecting and analyzing appropriate data is essential. As a result, computing winning rates for each match and various statistics to predict the winner of a future match, champion of the league, and top scorer can support building the strategy.

# High-Level approach
For the champion of the season prediction, we collected match histories from previous seasons and teams' overall ratings to predict future matches. With the collected datasets, we calculated the Head-to-Head ratio and the All-Time win ratio for each match and team. We trained a machine learning model with these ratios based on match histories and overall team ratings and used it to compute probabilities in future matches and to calculate the game points that the teams will earn at the end of the season.

For the top scorer prediction, we collected top scorer standings and data like how many goals they scored, shots made per game, goals made per shot, and minutes they played this season. With the data, we calculated the total goals scored per player at the end of the season, the player’s contribution to the team, and the efficiency of each player.

# Methodology
To begin the project, we conducted a comprehensive search for the datasets required. We collected data from a total of 8 seasons, including individual season data, current schedule data, and additional information obtained through web scraping using BeautifulSoup. This allowed us to gather overall scores, top scorer data, and team standings.

Once we had gathered all the necessary data, we proceeded to clean and filter it. Our initial step involved unifying team names across different datasets so that we could easily merge and concatenate the data based on team names. Specifically, we modified team names in the FIFA overall datasets to match those in the seasonal data and merged the corresponding years. We then combined all seasons, except for the current one, into a single dataframe and eliminated any unnecessary columns.

In order to prepare the data for machine learning analysis, we calculated the head-to-head ratio, which considers the historical performance of each team against individual opponents. This ratio provides insights into the teams' previous matchups. Additionally, we computed the overall winning ratio for home and away teams, which represents the number of wins divided by the total number of matches played.

Furthermore, we merged two datasets: the top scorer data and the current team standings. We only retained the top 100 players and relevant columns, discarding any unnecessary information.

To predict the winners of future rounds and the season's champion, we employed a machine learning model called Random Forest Classifier. Our training data consisted of all seasons except the current one, while the test data included the current season up to the point where the match occurred. We set the "FTR" (full-time result) column as the label, and the remaining columns served as features. After importing and training the model with the training features and labels, we evaluated its accuracy, which was approximately 52%. Subsequently, we utilized the model to predict match results for future matches. Based on these predictions, we calculated the total points earned by each team and updated their current standings accordingly.

# Dataset
Our datasets are from various sources and from the following links: 
<br>Seasonal data: https://www.football-data.co.uk/englandm.php
<br>FIFA overall data: https://www.fifaindex.com/teams/?league=13&order=desc
<br>Current Standing: https://www.msn.com/en-us/sports/soccer/premier-league/standings
<br>Top Scorer data: https://www.msn.com/en-us/sports/soccer/premier-league/player-stats/sp-s-gs
<br>Current season schedules: https://fixturedownload.com/results/epl-2020
