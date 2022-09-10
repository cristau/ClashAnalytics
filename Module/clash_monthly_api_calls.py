import requests
import pandas as pd
import numpy as np
import time
import os.path
from config import *


def get_player_achievements(player_tag):
    response = requests.get(
        'https://api.clashofclans.com/v1/players/%23' + player_tag, headers=headers)
    json_response = response.json()

    achievements_dict = json_response['achievements']

    if 'clan' in json_response:
        for i in achievements_dict:
            i.update({'clanName': json_response['clan']['name'], 'clanTag': json_response['clan']['tag']})
    if 'clan' not in json_response:
        for i in achievements_dict:
            i.update({'clanName': None, 'clanTag': None})

    achievements_df = pd.DataFrame(achievements_dict)

    return achievements_dict


def get_member_ach_info():
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

        ls = [get_player_achievements(i) for i in member_list]
        ach_master.extend(ls)

        print('\tDone with ' + json_response['name'] + '...')

    print('Successfully pulled achievement info for all players in all clans.')

    all_dfs = []
    for i in ach_master:
        df = pd.DataFrame(i)
        all_dfs.append(df)

    ach_info_df = pd.concat(all_dfs)
    ach_info_df['datePulled'] = np.repeat(time.strftime('%m-%d-%Y'), len(ach_info_df))

    print('Dumping to SQL and writing to Output path...')
    ach_info_df.to_sql(
        name='ach_member_info',
        con=connection,
        if_exists='append',
        index=False
    )

    if os.path.exists(f'Output/ach_info_df.csv'):
        ach_info_df.to_csv(f'Output/ach_info_df.csv', index=False, header=False, mode='a')
    else:
        ach_info_df.to_csv(f'Output/ach_info_df.csv', index=False)

    print('Successfully dumped achievement info.')

    return ach_info_df


def main():
    get_member_ach_info()


if __name__ == '__main__':
    main()
