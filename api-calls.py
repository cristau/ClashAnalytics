import requests
import pandas as pd
import json
from api_headers import headers

#clan_tag = 9VG8P90Q
#player_tag = QVGGVC02

# returns information regarding player info from the clan response (this only pulls player info that we cannot get from the player response)
def get_player_info_from_clan(clan_tag):
    response = requests.get(
        'https://api.clashofclans.com/v1/clans/%23' + clan_tag, headers = headers)
    json_response = response.json()
    rows = []
    for i in json_response['memberList']:
        rows.append([i['tag'], i['clanRank'], i['previousClanRank']])
    return(rows)

df1 = pd.DataFrame(get_player_info_from_clan('9VG8P90Q'), columns = ["player_tag", "clan_rank", "previous_clan_rank"])
print(df1)

# returns information regarding player info from the player response
def get_player_info(player_tag):
    response = requests.get(
        'https://api.clashofclans.com/v1/players/%23' + player_tag, headers = headers)
    json_response = response.json()
    rows = []
    rows.append([json_response['tag'], json_response['name'], json_response['townHallLevel'], json_response['townHallWeaponLevel'],
                 json_response['expLevel'], json_response['trophies'], json_response['bestTrophies'], json_response['warStars'],
                 json_response['attackWins'], json_response['defenseWins'], json_response['builderHallLevel'], json_response['versusTrophies'],
                 json_response['bestVersusTrophies'], json_response['versusBattleWins'], json_response['role'], json_response['warPreference'],
                 json_response['donations'], json_response['donationsReceived'], json_response['clan']['tag'], json_response['clan']['name'],
                 json_response['clan']['clanLevel'], json_response['league']['name']])
    return(rows)

df2 = pd.DataFrame(get_player_info('QVGGVC02'), columns = [
    'player_tag', 'player_name', 'th_lvl', 'th_weapon_lvl', 'exp_lvl', 'trophies', 'best_trophies', 'war_stars',
                                                           'attack_wins', 'defense_wins', 'bldr_hall_lvl', 'vs_trophies', 'best_vs_trophies', 'vs_battle_wins', 'role',
                                                           'war_pref', 'donations', 'donations_rec', 'clan_tag', 'clan_name', 'clan_level', 'league_name'])
print(df2)

# returns a players troop information with their corresponding player tag
def get_player_troop_info(player_tag):
    response = requests.get(
        'https://api.clashofclans.com/v1/players/%23' + player_tag, headers = headers)
    json_response = response.json()
    rows = []
    for i in json_response['troops']:
        rows.append([json_response['tag'], i['name'], i['level'], i['maxLevel'], i['village']])

    return(rows)

df3 = pd.DataFrame(get_player_troop_info('QVGGVC02'), columns = [
    'player_tag', 'troop_name', 'troop_lvl', 'max_lvl', 'village'
])
print(df3)

def get_all_clan_member_info(clan_tag):
    '''
    Grabs player information from the player response, but for every member in a given clan
    :param clan_tag: a clan tag string
    :return: A dataframe
    '''