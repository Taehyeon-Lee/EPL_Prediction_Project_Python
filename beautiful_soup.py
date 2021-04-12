from bs4 import BeautifulSoup
import requests
import csv


def scrap_overall(url, file_name):
    """
    Scrap data for team overall ratings over seasons 2013-14 to 2020-21
    from a website using Beautiful Soup
    """
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    new_file = csv.writer(open(file_name, "w", encoding='utf-8', newline=''))
    new_file.writerow(["Team", "Overall"])

    for tr in soup.findAll("tr"):
        names = tr.findAll("td", {"data-title": "Name"})
        overalls = tr.findAll("td", {"data-title": "OVR"})
        if names == []:
            pass
        else:
            new_file.writerow([names[0].text, overalls[0].text])


def scrap_top_scorer(url, file_name):
    """
    Scrap data for scorers statistics data in 2020-21 season
    from a website using Beautiful Soup
    """
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")

    new_file = csv.writer(open(file_name, "w", encoding='utf-8', newline=''))
    new_file.writerow(["Rank", "Player", "Team", "logo", "Game Played", "GS",
                       "Minutes Played", "Goals", "AS", "Shots", "SOG"])
    for tr in soup.findAll("tr", {"class": "rowlink"}):
        tds = tr.find_all("td")
        try:
            rank = tds[0].text
            player = tds[1].text
            team = tds[2].text
            logo = tds[3].text
            game_played = tds[4].text
            GS = tds[5].text
            Minute = tds[6].text
            Goals = tds[7].text
            AS = tds[8].text
            shots = tds[9].text
            sog = tds[10].text

        except:
            print("bad tr string: {}".format(tds))
            continue

        new_file.writerow([rank, player, team, logo, game_played,
                           GS, Minute, Goals, AS, shots, sog])


def scrap_standing(url, file_name):
    """
    Scrap data for current team standing in 2020-21 season '
    from a website using Beautiful Soup
    """
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")

    new_file = csv.writer(open(file_name, "w", encoding='utf-8', newline=''))
    new_file.writerow(["Rank", "Team", "Game Played", "W", "D", "L",
                       "Team Goals", "GA", "GD", "PTS"])
    for tr in soup.findAll("tr", {"class": "rowlink"}):
        tds = tr.find_all("td")
        try:
            rank = tds[0].text
            team = tds[2].text
            game_played = tds[3].text
            win = tds[4].text
            draw = tds[5].text
            loss = tds[6].text
            goal_for = tds[7].text
            goal_against = tds[8].text
            goal_diff = tds[9].text
            points = tds[10].text

        except:
            print("bad tr string: {}".format(tds))
            continue

        new_file.writerow([rank, team, game_played, win, draw, loss, goal_for,
                           goal_against, goal_diff, points])
