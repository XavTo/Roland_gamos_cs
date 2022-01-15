import sys
import time
import requests
from bs4 import BeautifulSoup


def get_parsed_page(url):
    headers = {
        "referer": "https://www.hltv.org/stats",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

def _find_lineup(team_name, team_id, player_1, player_2):
    page = get_parsed_page(f"https://www.hltv.org/stats/teams/lineups/{team_id}/a")
    list_teammate_lineup = []
    lineup_containers = page.find_all("div", {"class": "lineup-container"})
    played_together = False
    for lineup_container in lineup_containers:
        lineup = lineup_container.find_all("div", {"class": "col teammate"})
        for teammate in lineup:
            list_teammate_lineup.append(teammate.find("div", {"class": "text-ellipsis"}).text.lower())
        if player_1 and player_2 in list_teammate_lineup:
            print("They played together in " + team_name + " (" + lineup_container.find_all("span", {"data-time-format": "MMM yyyy"})[0].text
                    + "-" + lineup_container.find_all("span", {"data-time-format": "MMM yyyy"})[1].text + ") " + str(list_teammate_lineup))
            played_together = True
        list_teammate_lineup = []
    if not played_together:
        print("They not played together in " + team_name)
    return played_together


def players_played_together(player_id, name_second_player, time_sleep = 0.3):
    played_together = False
    page = get_parsed_page(f"https://www.hltv.org/player/{player_id}/a#tab-teamsBox")
    name_first_player = page.find("h1", {"class": "playerNickname"}).text
    list_team_id = [page.find("table", {"class": "table-container team-breakdown"}).find("tbody").find("tr", {"class": "team"})
                    .find("td", {"class": "team-name-cell"}).find('a')['href'].split("/")[2]]
    list_team_name = [page.find("table", {"class": "table-container team-breakdown"}).find("tbody").find("tr", {"class": "team"})
                    .find("td", {"class": "team-name-cell"}).find('a')['href'].split("/")[3]]
    teams = page.find("table", {"class": "table-container team-breakdown"}).find("tbody").find_all("tr", {"class": "team past-team"})
    for team in teams:
        list_team_id.append(team.find("td", {"class": "team-name-cell"}).find('a')['href'].split("/")[2])
        list_team_name.append(team.find("td", {"class": "team-name-cell"}).find('a')['href'].split("/")[3])
    for team_id, team_name in zip(list_team_id, list_team_name):
        if _find_lineup(team_name, team_id, name_first_player, name_second_player):
            played_together = True
        time.sleep(time_sleep)
    return played_together


def find_id_from_name(player_name, time_sleep = 0.3):
    page = get_parsed_page(f"https://www.hltv.org/search?query={player_name}")
    time.sleep(time_sleep)
    return page.find("table", {"class": "table"}).find('a')['href'].split("/")[2]


if len(sys.argv) == 5:
    if sys.argv[3] == "-s":
        first_player_name = sys.argv[1].lower()
        first_player_id = find_id_from_name(first_player_name, float(sys.argv[4]))
        second_player = sys.argv[2].lower()
        players_played_together(first_player_id, second_player, float(sys.argv[4]))



if len(sys.argv) == 3:
    first_player_name = sys.argv[1].lower()
    first_player_id = find_id_from_name(first_player_name)
    second_player = sys.argv[2].lower()
    players_played_together(first_player_id, second_player)