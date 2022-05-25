import requests

headers = {
    'Accept': 'application/json',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjFlN2I2ZjAyLTIwM2EtNDcwMy1iODAyLTA2OWUzMGQ4ZmZmMiIsImlhdCI6MTY1MzM5ODcwMSwic3ViIjoiZGV2ZWxvcGVyLzRlOGFmYmIzLWYzOTItY2YwNC1kYjE4LTQxZDYyNGY5MWQ0NyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjk4LjU5LjExMy4yNyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.YqWY4HQ_gkQLtrTxT28vOnjg19BVRTkJa2eVInFn_JyizjVod1JIsfNeifb5XAZaZCae79WYhHXetF6A3vBHEQ'
}

def get_clan_info(clan_tag):
    response = requests.get(
        'https://api.clashofclans.com/v1/clans/%23' + clan_tag, headers = headers)
    player_info_json = response.json()
    print(player_info_json)
get_clan_info('9VG8P90Q')
