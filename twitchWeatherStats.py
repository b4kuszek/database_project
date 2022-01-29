import pymysql

# Connecting to Twitch&Weather
connection_TW = pymysql.connect(host="localhost", user="root", passwd="", database="Twitch&Weather")
cursor_TW = connection_TW.cursor()

# Connecting to Twitch&Weather&Stats
connection_TWS = pymysql.connect(host="localhost", user="root", passwd="", database="Twitch&Weather&Stats")
cursor_TWS = connection_TWS.cursor()

####################################################################
# Streamers tables
streamers = ['overpow', 'ewroon', 'popo', 'nervarien', 'vysotzky', 'pago3', 'izakooo', 'rybsonlol_',
             'polsatgames', 'xth0rek', 'xqcow', 'trainwreckstv', 'lirik', 'loltyler1', 'sodapoppin',
             'shroud', 'pokimane', 'fextralife', 'summit1g', 'forsen']

####################################################################
# Add streamers
for streamer in streamers:

    cursor_TWS.execute(f"SHOW TABLES LIKE '{streamer}'")
    output = cursor_TWS.fetchall()

    if len(output) == 0:
        cursor_TWS.execute(f"""CREATE TABLE {streamer}(
                            ID INT(20) PRIMARY KEY AUTO_INCREMENT,
                            AVG_FROM DATETIME(0) NOT NULL,
                            AVG_TO DATETIME(0) NOT NULL,
                            TITLE CHAR(20),
                            AVERAGE_VIEWERS INT(20),
                            CITY CHAR(20),
                            WEATHER_INFO CHAR(20),
                            TEMPERATURE INT(20)
                            )""")

####################################################################
# Gathering queries

for streamer in streamers:

    big_query = f"""SELECT avg_viewers_pl.AVG_FROM, avg_viewers_pl.AVG_TO, games.TITLE, avg_viewers_pl.AVG_VIEWERS, 
                    weather_pl.CITY, weather_pl.GENERAL_INFO, weather_pl.TEMP FROM streamer_pl 
                    INNER JOIN games ON games.ID = streamer_pl.GAME_ID 
                    INNER JOIN avg_viewers_pl ON avg_viewers_pl.STREAMER_PL_ID = streamer_pl.ID_pl 
                    INNER JOIN weather_pl ON weather_pl.AVG_VIEWERS_PL_ID = avg_viewers_pl.ID 
                    WHERE streamer_pl.NAME = "{streamer}";"""

    cursor_TW.execute(big_query)
    streamer_stats = cursor_TW.fetchall()

    # Checking if data exists in the table
    if len(streamer_stats) != 0:
        check_if_exists = f"SELECT EXISTS(SELECT * FROM {streamer} where avg_from = '" + str(streamer_stats[0][0]) + "')"
        cursor_TWS.execute(check_if_exists)
        boolean_streamer = cursor_TWS.fetchall()

    # Inserting queries
    addStreamerStats = f"""INSERT INTO {streamer} (AVG_FROM, AVG_TO, TITLE, AVERAGE_VIEWERS, CITY, WEATHER_INFO, TEMPERATURE)
                      VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    # Inserting data
    if len(streamer_stats) != 0:
        if boolean_streamer[0][0] == 0:
            cursor_TWS.executemany(addStreamerStats, streamer_stats)

####################################################################
# Closing connections
connection_TW.commit()
connection_TW.close()

connection_TWS.commit()
connection_TWS.close()