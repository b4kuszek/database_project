import pymysql
import json
import requests

URL = 'https://api.twitch.tv/helix/games/top'

headers = {
    'Authorization': 'Bearer 9n6j9z9e1zx3g1jc8ajdguya24y88s',
    'Client-Id': 'v8dly98x0oe9wdmyvgqo3el4s5g12p',
}

response = requests.get(URL, headers=headers).json()

games = []

for i in range(20):
    games.append((response['data'][i]['name'], i+1))

######################################################################

# Connecting to DB
connection = pymysql.connect(host="localhost", user="root", passwd="", database="Twitch&Weather")
cursor = connection.cursor()

# Opening file with data
f = open('Average_Viewers_EN.json')
data = json.load(f)

streamers_en = list(data.keys())[2:]

# Queries
addGames = 'INSERT INTO games (TITLE, RANK) VALUES (%s, %s)'

# Inserting data
cursor.executemany(addGames, games)

connection.commit()
connection.close()