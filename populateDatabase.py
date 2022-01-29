import pymysql
import json
import requests

Games_URL = 'https://api.twitch.tv/helix/games/top'
Streamers_URL = 'https://api.twitch.tv/helix/streams'

headers = {
    'Authorization': 'Bearer xnzpq6d45ptdy4ul5egcr2mmy9wk21',
    'Client-Id': 'v8dly98x0oe9wdmyvgqo3el4s5g12p',
}

params_EN = (
    ('user_login', ['xqcow', 'trainwreckstv', 'lirik', 'loltyler1', 'sodapoppin', 'shroud', 'pokimane', 'fextralife', 'summit1g', 'forsen']),
)

params_PL = (
    ('user_login', ['overpow', 'ewroon', 'popo', 'nervarien', 'vysotzky', 'pago3', 'izakooo', 'RybsonLoL_', 'polsatgames', 'xth0rek']),
)

# Connecting to DB
connection = pymysql.connect(host="localhost", user="root", passwd="", database="Twitch&Weather")
cursor = connection.cursor()

# Responses

Games_response = requests.get(Games_URL, headers=headers).json()
Streamers_EN_response = requests.get(Streamers_URL, headers=headers, params=params_EN).json()
Streamers_PL_response = requests.get(Streamers_URL, headers=headers, params=params_PL).json()

# Responses formatting

### Games

games = []

for i in range(20):

    game_name = Games_response['data'][i]['name']
    game_id = Games_response['data'][i]['id']

    retrieve = "SELECT EXISTS(SELECT * FROM games where twitch_game_id = " + game_id + ")"
    cursor.execute(retrieve)
    rows = cursor.fetchall()

    if rows[0][0] == 0:
        games.append((game_name, game_id))

### Streamers English

streamers_en = []

for i in range(len(Streamers_EN_response['data'])):

    game_id = Streamers_EN_response['data'][i]['game_id']
    game_name = Streamers_EN_response['data'][i]['game_name']
    streamer_name = Streamers_EN_response['data'][i]['user_name']

    # Retrieving game_id
    retrieve = "SELECT * FROM games where twitch_game_id = " + game_id
    cursor.execute(retrieve)
    rows = cursor.fetchall()

    # Checking if streamer exists in the table
    check_if_exists = "SELECT EXISTS(SELECT * FROM streamer_en where name = '" + streamer_name + "')"
    cursor.execute(check_if_exists)
    boolean = cursor.fetchall()

    # Checking if the game changed
    check_if_new_game = "SELECT * FROM streamer_en where name = '" + streamer_name + "'"
    cursor.execute(check_if_new_game)
    old_game = cursor.fetchall()

    # Adding game to games if not in top 20
    if len(rows) == 0:
        games.append((game_name, game_id))

    # Updating game if new
    if len(old_game) != 0:
        if old_game[0][3] != game_id:
            update = f"""UPDATE streamer_en
                            SET current_twitch_game_id = {game_id}
                            WHERE current_twitch_game_id = {str(old_game[0][3])};"""
            cursor.execute(update)

    # Appending only when streamer is not already in the table
    if len(rows) != 0 and boolean[0][0] == 0:
        streamers_en.append((streamer_name, rows[0][0], game_id))

### Streamers Polish

streamers_pl = []

for i in range(len(Streamers_PL_response['data'])):

    game_id = Streamers_PL_response['data'][i]['game_id']
    streamer_name = Streamers_PL_response['data'][i]['user_name']

    # Retrieving game_id
    retrieve = "SELECT * FROM games where twitch_game_id = " + game_id
    cursor.execute(retrieve)
    rows = cursor.fetchall()

    # Checking if streamer exists in the table
    check_if_exists = "SELECT EXISTS(SELECT * FROM streamer_pl where name = '" + streamer_name + "')"
    cursor.execute(check_if_exists)
    boolean = cursor.fetchall()

    # Checking if the game changed
    check_if_new_game = "SELECT * FROM streamer_pl where name = '" + streamer_name + "'"
    cursor.execute(check_if_new_game)
    old_game = cursor.fetchall()

    # Updating game if new
    if len(old_game) != 0:
        if old_game[0][3] != game_id:
            update = f"""UPDATE streamer_pl
                        SET current_twitch_game_id = {game_id}
                        WHERE current_twitch_game_id = {str(old_game[0][3])};"""
            cursor.execute(update)

    # Appending only when streamer is not already in the table
    if len(rows) != 0 and boolean[0][0] == 0:
        streamers_pl.append((streamer_name, rows[0][0], game_id))

#####################################################################################################

# Queries
addGames = 'INSERT INTO games (TITLE, TWITCH_GAME_ID) VALUES (%s, %s)'
addStreamersEN = 'INSERT INTO streamer_en (NAME, GAME_ID, CURRENT_TWITCH_GAME_ID) VALUES (%s, %s, %s)'
addStreamersPL = 'INSERT INTO streamer_pl (NAME, GAME_ID, CURRENT_TWITCH_GAME_ID) VALUES (%s, %s, %s)'

# Inserting data
cursor.executemany(addGames, games)
cursor.executemany(addStreamersEN, streamers_en)
cursor.executemany(addStreamersPL, streamers_pl)

# Close connection
connection.commit()
connection.close()