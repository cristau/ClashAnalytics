import requests
import pandas as pd
import numpy as np
import time
import os.path
from config import *


def get_player_info(player_tag):
    try:
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
    except Exception as e:
        print(e)


def get_basic_member_info():
    try:
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
        all_member_data_df.columns = all_member_data_df.columns.str.lower()

        print('Writing to Output path and dumping to SQL...')

        if os.path.exists(f'Output/basic_member_info.csv'):
            all_member_data_df.to_csv(f'Output/basic_member_info.csv', index=False, header=False, mode='a')
        else:
            all_member_data_df.to_csv(f'Output/basic_member_info.csv', index=False)
        print('Successfully wrote all basic member info to Output path.')

        with engine.connect() as conn:
            all_member_data_df.to_sql(
                name='basic_member_info',
                con=conn,
                if_exists='append',
                index=False
            )
        print('Successfully dumped all basic member info to SQL.')

        return all_member_data_df
    except Exception as e:
        print(e)


def main():
    get_basic_member_info()


if __name__ == '__main__':
    main()
