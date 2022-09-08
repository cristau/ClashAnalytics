import requests
import pandas as pd
import numpy as np
import time
import os.path
from config import *

clan_tags_dict = {
    'Invidia Bandit': '9VG8P90Q', 'Rob-Seb': '8Q0L9CRY', 'Vi11ageWarriors': 'LL2C8L8V', '#THE SHIELD#': 'PGPPQRLY',
    'Immortal Rising': '28Q99QL0Q', 'No Mercy': 'LLJCVJQL', 'Indian Prestige': 'PQJUJCPL'}


def get_ls_info(player_tag):
    try:
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
    except Exception as e:
        print(e)


def get_ls_member_info():
    try:
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
            subset=['legendTrophies', 'bestSeasonRank', 'bestSeasonTrophies', 'bestSeasonDate', 'previousSeasonRank',
                    'previousSeasonTrophies', 'currentSeasonRank', 'previousSeasonDate'], how='all')
        ls_member_info_df['datePulled'] = np.repeat(time.strftime('%m-%d-%Y'), len(ls_member_info_df))

        print('Writing to Output path and dumping to SQL...')

        if os.path.exists(f'Output/ls_member_info.csv'):
            ls_member_info_df.to_csv(f'Output/ls_member_info.csv', index=False, header=False, mode='a')
        else:
            ls_member_info_df.to_csv(f'Output/ls_member_info.csv', index=False)
        print('Successfully wrote all basic member info to Output path.')

        with engine.connect() as conn:
            ls_member_info_df.to_sql(
                name='ls_member_info',
                con=conn,
                if_exists='append',
                index=False
            )
        print('Successfully dumped legend statistics info to SQL.')

        return ls_member_info_df
    except Exception as e:
        print(e)

# def get_player_achievements(player_tag):
#     response = requests.get(
#         'https://api.clashofclans.com/v1/players/%23' + player_tag, headers=headers)
#     json_response = response.json()
#
#     achievements_dict = json_response['achievements']
#
#     # needed to include the if statement to not overwrite clanName and clanTag with every iteration if clanName
#     # and clanTag exist
#     for i in achievements_dict:
#         if 'clanName' and 'clanTag' not in i:
#             i.update({'name': json_response['name'], 'tag': json_response['tag']})
#
#     achievements_df = pd.DataFrame(achievements_dict)
#
#     return achievements_dict
#
#
# def get_member_achievements():
#     print("Pulling achievement info...")
#     ach_master = []
#     for clan in clan_tags_dict.values():
#         response = requests.get(
#             'https://api.clashofclans.com/v1/clans/%23' + clan, headers=headers)
#         json_response = response.json()
#
#         temp = []
#         for i in json_response['memberList']:
#             temp.append(i['tag'])
#
#         member_list = [i.replace('#', '') for i in temp]
#
#         ls = [get_player_achievements(i) for i in member_list]
#         ach_master.extend(ls)
#
#         print('\tDone with ' + json_response['name'] + '...')
#
#     print('Successfully pulled achievement info for all players in all clans.')
#
#     ach_info_df = pd.DataFrame(ach_master)
#     ach_info_df['datePulled'] = np.repeat(time.strftime('%m-%d-%Y'), len(ach_info_df))
#
#     print('Dumping to SQL and writing to Output path...')
#     ach_info_df.to_sql(
#         name='ach_info_df',
#         con=connection,
#         if_exists='append',
#         index=False
#     )
#
#     if os.path.exists(f'Output/ach_info_df.csv'):
#         ach_info_df.to_csv(f'Output/ach_info_df.csv', index=False, header=False, mode='a')
#     else:
#         ach_info_df.to_csv(f'Output/ach_info_df.csv', index=False)
#
#     print('Successfully dumped achievement info.')
#
#     return ach_info_df


def main():
    get_ls_member_info()


if __name__ == '__main__':
    main()
