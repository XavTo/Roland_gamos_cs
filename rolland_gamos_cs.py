import sys
import time
import requests
from bs4 import BeautifulSoup


def find_id_from_name(player_name, time_sleep = 0.3):
    page = get_parsed_page(f"https://www.hltv.org/search?query={player_name}")
    time.sleep(time_sleep)
    return page.find("table", {"class": "table"}).find('a')['href'].split("/")[2].lower()


def get_parsed_page(url):
    headers = {
        "referer": "https://www.hltv.org/stats",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

def _find_lineup(team_name, team_id, player_1, player_2, display):
    page = get_parsed_page(f"https://www.hltv.org/stats/teams/lineups/{team_id}/a")
    list_teammate_lineup = []
    lineup_containers = page.find_all("div", {"class": "lineup-container"})
    played_together = False
    for lineup_container in lineup_containers:
        lineup = lineup_container.find_all("div", {"class": "col teammate"})
        for teammate in lineup:
            list_teammate_lineup.append(teammate.find("div", {"class": "text-ellipsis"}).text.lower().replace("-", ""))
        if player_1 in list_teammate_lineup and player_2 in list_teammate_lineup:
            if display:
                try:
                    print("They played together in " + team_name + " (" + lineup_container.find_all("span", {"data-time-format": "MMM yyyy"})[0].text
                            + "-" + lineup_container.find_all("span", {"data-time-format": "MMM yyyy"})[1].text + ") " + str(list_teammate_lineup))
                except IndexError:
                    print("They played together in " + team_name + " (" + lineup_container.find_all("span", {"data-time-format": "MMM yyyy"})[0].text
                            + "-present) " + str(list_teammate_lineup))
            played_together = True
        list_teammate_lineup = []
    if not played_together and display:
        print("They not played together in " + team_name)
    return played_together


def players_played_together(name_first_player, name_second_player, display = True, time_sleep = 0.3):
    player_id = find_id_from_name(name_first_player, time_sleep)
    played_together = False
    page = get_parsed_page(f"https://www.hltv.org/player/{player_id}/a#tab-teamsBox")
    name_first_player = page.find("h1", {"class": "playerNickname"}).text.replace("-", "")
    list_team_id = [page.find("table", {"class": "table-container team-breakdown"}).find("tbody").find("tr", {"class": "team"})
                    .find("td", {"class": "team-name-cell"}).find('a')['href'].split("/")[2]]
    list_team_name = [page.find("table", {"class": "table-container team-breakdown"}).find("tbody").find("tr", {"class": "team"})
                    .find("td", {"class": "team-name-cell"}).find('a')['href'].split("/")[3]]
    teams = page.find("table", {"class": "table-container team-breakdown"}).find("tbody").find_all("tr", {"class": "team past-team"})
    for team in teams:
        list_team_id.append(team.find("td", {"class": "team-name-cell"}).find('a')['href'].split("/")[2])
        list_team_name.append(team.find("td", {"class": "team-name-cell"}).find('a')['href'].split("/")[3])
    for team_id, team_name in zip(list_team_id, list_team_name):
        if _find_lineup(team_name, team_id, name_first_player.lower(), name_second_player.lower(), display):
            played_together = True
        time.sleep(time_sleep)
    return played_together
