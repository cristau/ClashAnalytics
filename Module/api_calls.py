import requests
import pandas as pd
import numpy as np
import time
import os.path
from Module.config import *

clan_tags_dict = {
    'Invidia Bandit': '9VG8P90Q', 'Rob-Seb': '8Q0L9CRY', 'Vi11ageWarriors': 'LL2C8L8V', '#THE SHIELD#': 'PGPPQRLY',
    'Immortal Rising': '28Q99QL0Q', 'No Mercy': 'LLJCVJQL', 'Indian Prestige': 'PQJUJCPL'}


def get_player_info(player_tag):
    response = requests.get(
        'https://api.clashofclans.com/v1/players/%23' + player_tag, headers=headers)
    json_response = response.json()

    breaking_list = ['clan', 'league', 'legendStatistics', 'achievements', 'versusBattleWinCount', 'labels', 'troops',
                     'heroes', 'spells']
    missing_col = ['townHallWeaponLevel', 'role', 'warPreference']

    player_dict = {}
    for k, v in zip(json_response.keys(), json_response.values()):
        if k in breaking_list:
            break
        player_dict.update({k: v})
    if not any(i in missing_col for i in list(player_dict.keys())):
        for i in missing_col:
            player_dict.update({i: None})
    if 'league' not in json_response:
        player_dict.update({'league': None})
    else:
        player_dict.update({'league': json_response['league']['name']})

    player_df = pd.DataFrame(player_dict, index=[0])
    return player_dict


def get_basic_member_info():
    print("Pulling basic member info...")
    bmi_master = []
    for clan in clan_tags_dict.values():
        response = requests.get(
            'https://api.clashofclans.com/v1/clans/%23' + clan, headers=headers)
        json_response = response.json()

        temp = []
        for i in json_response['memberList']:
            temp.append(i['tag'])

        member_list = [i.replace('#', '') for i in temp]

        players = [get_player_info(i) for i in member_list]
        bmi_master.extend(players)

        # needed to include the if statement to not overwrite clanName and clanTag with every iteration if clanName
        # and clanTag exist
        for i in bmi_master:
            if 'clanName' and 'clanTag' not in i:
                i.update({'clanName': json_response['name'], 'clanTag': json_response['tag']})

        print('\tDone with ' + json_response['name'] + '...')

    print('Successfully pulled basic member info for all players in all clans.')

    all_member_data_df = pd.DataFrame(bmi_master)
    all_member_data_df['datePulled'] = np.repeat(time.strftime('%m-%d-%Y'), len(bmi_master))

    print('Dumping to SQL and writing to Input path...')
    all_member_data_df.to_sql(
        name='basic_member_info',
        con=connection,
        if_exists='append',
        index=False
    )

    if os.path.exists(f'Input/basic_member_info.csv'):
        all_member_data_df.to_csv(f'Input/basic_member_info.csv', index=False, header=False, mode='a')
    else:
        all_member_data_df.to_csv(f'Input/basic_member_info.csv', index=False)

    print('Successfully dumped all basic member info.')

    return all_member_data_df


def get_ls_info(player_tag):
    response = requests.get(
        'https://api.clashofclans.com/v1/players/%23' + player_tag, headers=headers)
    json_response = response.json()

    ls_dict = {}
    if 'legendStatistics' in json_response:
        ls_dict.update({'tag': json_response['tag'],
                        'name': json_response['name']})
        if 'bestSeason' in json_response['legendStatistics']:
            ls_dict.update({'legendTrophies': json_response['legendStatistics']['legendTrophies'],
                            'bestSeasonDate': json_response['legendStatistics']['bestSeason']['id'],
                            'bestSeasonRank': json_response['legendStatistics']['bestSeason']['rank'],
                            'bestSeasonTrophies': json_response['legendStatistics']['bestSeason']['trophies']})

        if 'previousSeason' in json_response['legendStatistics']:
            ls_dict.update({'previousSeasonDate': json_response['legendStatistics']['previousSeason']['id'],
                            'previousSeasonRank': json_response['legendStatistics']['previousSeason']['rank'],
                            'previousSeasonTrophies': json_response['legendStatistics']['previousSeason']['trophies']})
        else:
            ls_dict.update({'previousSeasonDate': None,
                            'previousSeasonRank': None,
                            'previousSeasonTrophies': None})

        if 'rank' in json_response['legendStatistics']['currentSeason']:
            ls_dict.update({'currentSeasonRank': json_response['legendStatistics']['currentSeason']['rank'],
                            'currentSeasonTrophies': json_response['legendStatistics']['currentSeason']['trophies']})
        else:
            ls_dict.update({'currentSeasonRank': None,
                            'currentSeasonTrophies': json_response['legendStatistics']['currentSeason']['trophies']})

    ls_df = pd.DataFrame(ls_dict, index=[0])

    return ls_dict


def get_ls_member_info():
    print("Pulling legend statistics info...")
    ls_master = []
    for clan in clan_tags_dict.values():
        response = requests.get(
            'https://api.clashofclans.com/v1/clans/%23' + clan, headers=headers)
        json_response = response.json()

        temp = []
        for i in json_response['memberList']:
            temp.append(i['tag'])

        member_list = [i.replace('#', '') for i in temp]

        ls = [get_ls_info(i) for i in member_list]
        ls_master.extend(ls)

        # checks if every dictionary in the list of dictionaries in ls_master are empty and discards the empty ones
        ls_master = [i for i in ls_master if i]

        # needed to include the if statement to not overwrite clanName and clanTag with every iteration if clanName
        # and clanTag exist
        for i in ls_master:
            if 'clanName' and 'clanTag' not in i:
                i.update({'clanName': json_response['name'], 'clanTag': json_response['tag']})

        print('\tDone with ' + json_response['name'] + '...')

    print('Successfully pulled legend statistics info for all players in all clans.')

    ls_member_info_df = pd.DataFrame(ls_master).dropna(
        subset=['legendTrophies', 'bestSeasonDate', 'bestSeasonRank', 'bestSeasonTrophies', 'previousSeasonDate',
                'previousSeasonRank', 'previousSeasonTrophies', 'currentSeasonRank'], how='all')
    ls_member_info_df['datePulled'] = np.repeat(time.strftime('%m-%d-%Y'), len(ls_member_info_df))

    print('Dumping to SQL and writing to Input path...')
    ls_member_info_df.to_sql(
        name='ls_member_info',
        con=connection,
        if_exists='append',
        index=False
    )

    if os.path.exists(f'Input/ls_member_info_df.csv'):
        ls_member_info_df.to_csv(f'Input/ls_member_info_df.csv', index=False, header=False, mode='a')
    else:
        ls_member_info_df.to_csv(f'Input/ls_member_info_df.csv', index=False)

    print('Successfully dumped legend statistics info.')

    return ls_member_info_df

def main():
    get_basic_member_info()
    get_ls_member_info()

if __name__ == '__main__':
    main()