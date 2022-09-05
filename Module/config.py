from sqlalchemy import create_engine

headers = {
    'Accept': 'application/json',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjUxOTViNTc1LWY1NmQtNDFiNS04OGExLTAzYTExM2E3ZmE5ZSIsImlhdCI6MTY1NDQwMzc2Niwic3ViIjoiZGV2ZWxvcGVyLzRlOGFmYmIzLWYzOTItY2YwNC1kYjE4LTQxZDYyNGY5MWQ0NyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjk4LjU5LjExOS4xMjYiLCI5OC41OS4xMTMuMjciXSwidHlwZSI6ImNsaWVudCJ9XX0.dOrbDnjIFeQlohn2KC37PFIgkgYoF3XtmfzL63zZrkKoW5GBBNRmbSnHnSvap-z9WX9znaWSnJcEOPiY7sbUcQ'
}

url = 'mysql://root:Fa9245a5afb97b@127.0.0.1/clash_analytics'
engine = create_engine(url)
connection = engine.connect()

# BabyHood
# player_tag = 'QJ8RPUCRL'

# top player
# player_tag = '9CRRUG009'

# MarketHood
# player_tag = 'QVGGVC02'

