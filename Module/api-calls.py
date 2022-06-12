import requests
import pandas as pd
import json
import numpy as np
from Module.api_headers import headers

#MarketHood
player_tag = 'QVGGVC02'

#BabyHood
player_tag = 'QJ8RPUCRL'

#Invidia Bandit
clan_tag = '9VG8P90Q'

#Indian Prestige
clan_tag = 'PQJUJCPL'

# def get_member_list(clan_tag):
#     response = requests.get(
#         'https://api.clashofclans.com/v1/clans/%23' + clan_tag, headers = headers)
#     json_response = response.json()
#
#     player_tags, player_names = [], []
#     for i in json_response['memberList']:
#         player_tags.append(i['tag'])
#         player_names.append(i['name'])
#
#     clan_tag = json_response['tag']
#     clan_name = json_response['name']
#
#     ML_dict = {'player_tag': player_tags, 'player_name': player_names, 'clan_tag': np.repeat(clan_tag, len(player_tags)), 'clan_name': np.repeat(clan_name, len(player_tags))}
#     ML_df = pd.DataFrame(ML_dict)
#     return(df)

#my_dict = {0: {'player_name': 'MarketHood', 'player_tag': MarketHood},
           # 1: {'player_name': 'BabyHood', 'player_tag': BabyHood}}


def get_player_info(player_tag):
    response = requests.get(
        'https://api.clashofclans.com/v1/players/%23' + player_tag, headers=headers)
    json_response = response.json()

    breaking_list = ['clan', 'league', 'legendStatistics', 'achievements', 'versusBattleWinCount', 'labels', 'troops', 'heroes', 'spells']
    missing_col = ['townHallWeaponLevel', 'role', 'warPreference']

    player_dict = {}
    for k, v in zip(json_response.keys(), json_response.values()):
        if k in breaking_list:
            break
        player_dict.update({k: v})
    if any(i in missing_col for i in list(player_dict.keys())) == False:
        for i in missing_col:
            player_dict.update({i: None})

    player_df = pd.DataFrame(player_dict, index = [0])
    return(player_dict)

def get_all_member_info(clan_tag):
    response = requests.get(
        'https://api.clashofclans.com/v1/clans/%23' + clan_tag, headers=headers)
    json_response = response.json()

    temp = []
    for i in json_response['memberList']:
        temp.append(i['tag'])

    member_list = [i.replace('#', '') for i in temp]

    players = [get_player_info(i) for i in member_list]
    all_member_data_df = pd.DataFrame(players)

    all_member_data_df['clan_name'] = np.repeat(json_response['name'], len(players))
    all_member_data_df['clan_tag'] = np.repeat(json_response['tag'], len(players))
    return(all_member_data_df)

print(get_all_member_info('9VG8P90Q'))