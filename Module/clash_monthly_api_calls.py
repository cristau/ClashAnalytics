import requests
import pandas as pd
import numpy as np
import time
import os.path
from config import *


def get_player_achievements(player_tag):
    try:
        response = requests.get(
            'https://api.clashofclans.com/v1/players/%23' + player_tag, headers=headers)
        json_response = response.json()

        achievements_dict = json_response['achievements']

        for i in achievements_dict:
            i.update({'playerName': json_response['name'], 'tag': json_response['tag']})

        if 'clan' in json_response:
            for i in achievements_dict:
                i.update({'clanName': json_response['clan']['name'], 'clanTag': json_response['clan']['tag']})
        if 'clan' not in json_response:
            for i in achievements_dict:
                i.update({'clanName': None, 'clanTag': None})

        achievements_df = pd.DataFrame(achievements_dict)

        return achievements_dict
    except Exception as e:
        print(e)


def get_member_ach_info():
    try:
        print("Pulling achievement info...")
        ach_master = []
        for clan in clan_tags_dict.values():
            response = requests.get(
                'https://api.clashofclans.com/v1/clans/%23' + clan, headers=headers)
            json_response = response.json()

            temp = []
            for i in json_response['memberList']:
                temp.append(i['tag'])

            member_list = [i.replace('#', '') for i in temp]

            ach = [get_player_achievements(i) for i in member_list]
            ach_master.extend(ach)

            print('\tDone with ' + json_response['name'] + '...')

        print('Successfully pulled achievement info for all players in all clans.')

        all_dfs = []
        for i in ach_master:
            df = pd.DataFrame(i)
            all_dfs.append(df)

        ach_member_info = pd.concat(all_dfs)
        ach_member_info['datePulled'] = np.repeat(time.strftime('%m-%d-%Y'), len(ach_member_info))
        ach_member_info.columns = ach_member_info.columns.str.lower()

        print('Dumping to SQL and writing to Output path...')
        with engine.connect() as conn:
            ach_member_info.to_sql(
                name='ach_member_info',
                con=conn,
                if_exists='append',
                index=False
            )

        if os.path.exists(f'Output/ach_member_info.csv'):
            ach_member_info.to_csv(f'Output/ach_member_info.csv', index=False, header=False, mode='a')
        else:
            ach_member_info.to_csv(f'Output/ach_member_info.csv', index=False)

        print('Successfully dumped achievement info.')

        return ach_member_info
    except Exception as e:
        print(e)


def get_player_troops(player_tag):
    try:
        response = requests.get(
            'https://api.clashofclans.com/v1/players/%23' + player_tag, headers=headers)
        json_response = response.json()

        troops_dict = json_response['troops']

        for i in troops_dict:
            i.update({'playerName': json_response['name'], 'tag': json_response['tag']})

        if 'clan' in json_response:
            for i in troops_dict:
                i.update({'clanName': json_response['clan']['name'], 'clanTag': json_response['clan']['tag']})
        if 'clan' not in json_response:
            for i in troops_dict:
                i.update({'clanName': None, 'clanTag': None})

        troops_df = pd.DataFrame(troops_dict)

        return troops_dict
    except Exception as e:
        print(e)


def get_member_troops_info():
    try:
        print("Pulling member troops info...")
        troops_master = []
        for clan in clan_tags_dict.values():
            response = requests.get(
                'https://api.clashofclans.com/v1/clans/%23' + clan, headers=headers)
            json_response = response.json()

            temp = []
            for i in json_response['memberList']:
                temp.append(i['tag'])

            member_list = [i.replace('#', '') for i in temp]

            troops = [get_player_troops(i) for i in member_list]
            troops_master.extend(troops)

            print('\tDone with ' + json_response['name'] + '...')

        print('Successfully pulled troops info for all players in all clans.')

        all_dfs = []
        for i in troops_master:
            df = pd.DataFrame(i)
            all_dfs.append(df)

        troops_info_df = pd.concat(all_dfs)
        troops_info_df['datePulled'] = np.repeat(time.strftime('%m-%d-%Y'), len(troops_info_df))
        troops_info_df.columns = troops_info_df.columns.str.lower()

        print('Dumping to SQL and writing to Output path...')
        with engine.connect() as conn:
            troops_info_df.to_sql(
                name='troops_member_info',
                con=conn,
                if_exists='append',
                index=False
            )
        if os.path.exists(f'Output/troops_info_df.csv'):
            troops_info_df.to_csv(f'Output/troops_info_df.csv', index=False, header=False, mode='a')
        else:
            troops_info_df.to_csv(f'Output/troops_info_df.csv', index=False)

        print('Successfully dumped troops info.')

        return troops_info_df
    except Exception as e:
        print(e)


def main():
    get_member_ach_info()
    get_member_troops_info()


if __name__ == '__main__':
    main()
