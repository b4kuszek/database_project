import pymysql
import json
import requests
import datetime

# Connecting to DB
connection = pymysql.connect(host="localhost", user="root", passwd="", database="Twitch&Weather")
cursor = connection.cursor()

# DEFINING FUNCTIONS ###################################################################

def CalcAverageViewers_EN():
    average_viewers = {}
    average_viewers['TimeStarted'] = time_started_EN
    average_viewers['TimeFinished'] = time_finished_EN

    for i in range(len(streamers_list_EN)):

        viewers_EN = []

        for streamer in data_EN['streamers']:
            viewers_EN.append(streamer[streamers_list_EN[i]])

        viewers_sum_EN = sum(viewers_EN)
        viewers_average_EN = viewers_sum_EN / len(viewers_EN)

        average_viewers[streamers_list_EN[i]] = viewers_average_EN

    return average_viewers

#######################################################################################

def CalcAverageViewers_PL():
    average_viewers = {}
    average_viewers['TimeStarted'] = time_started_PL
    average_viewers['TimeFinished'] = time_finished_PL

    for i in range(len(streamers_list_PL)):

        viewers_PL = []

        for streamer in data_PL['streamers']:
            viewers_PL.append(streamer[streamers_list_PL[i]])

        viewers_sum_PL = sum(viewers_PL)
        viewers_average_PL = viewers_sum_PL / len(viewers_PL)

        average_viewers[streamers_list_PL[i]] = viewers_average_PL

    return average_viewers

#######################################################################################
# Opening streamers files
try:
    f_EN = open('streamers_EN.json')
    f_PL = open('streamers_PL.json')

    data_EN = json.load(f_EN)
    data_PL = json.load(f_PL)
except:
    print("Cannot open a file!")

# Creating streamers lists
for streamer in data_EN['streamers']:
    streamers_list_EN = list(streamer.keys())[1:]

for streamer in data_PL['streamers']:
    streamers_list_PL = list(streamer.keys())[1:]

if len(data_EN['streamers'][0]) != 0:
    time_started_EN = (data_EN['streamers'][0]['Time'])
    time_finished_EN = (data_EN['streamers'][-1]['Time'])

if len(data_PL['streamers'][0]) != 0:
    time_started_PL = (data_PL['streamers'][0]['Time'])
    time_finished_PL = (data_PL['streamers'][-1]['Time'])

# RUNNING FUNCTIONS ###################################################################

if len(data_EN['streamers'][0]) != 0:
    average_viewers_EN = CalcAverageViewers_EN()

if len(data_PL['streamers'][0]) != 0:
    average_viewers_PL = CalcAverageViewers_PL()

#######################################################################################

# Getting English streamers names from file
streamers_names_EN = []
streamers_names_formatted_EN = []

if len(data_EN['streamers'][0]) != 0:
    for i in average_viewers_EN:
        streamers_names_EN.append(i)

    streamers_names_formatted_EN = streamers_names_EN[2:]

# Getting Polish streamers names from file
streamers_names_PL = []
streamers_names_formatted_PL = []

for i in average_viewers_PL:
    streamers_names_PL.append(i)

streamers_names_formatted_PL = streamers_names_PL[2:]

########################################################

avgViewersEN = []
avgViewersPL = []

# Retrieve dates for English streamers
# Retrieve average from
if len(data_EN['streamers'][0]) != 0:
    avg_from = average_viewers_EN['TimeStarted']
    avg_from_formatted_EN = datetime.datetime(int(avg_from[6:10]), int(avg_from[3:5]), int(avg_from[0:2]),
                                           int(avg_from[11:13]), int(avg_from[14:16]), int(avg_from[17:19]))

# Retrieve average to
if len(data_EN['streamers'][0]) != 0:
    avg_to = average_viewers_EN['TimeFinished']
    avg_to_formatted_EN = datetime.datetime(int(avg_to[6:10]), int(avg_to[3:5]), int(avg_to[0:2]),
                                         int(avg_to[11:13]), int(avg_to[14:16]), int(avg_to[17:19]))

###########################################################################################################

# Retrieve dates for Polish streamers
# Retrieve average from
if len(data_PL['streamers'][0]) != 0:
    avg_from = average_viewers_PL['TimeStarted']
    avg_from_formatted_PL = datetime.datetime(int(avg_from[6:10]), int(avg_from[3:5]), int(avg_from[0:2]),
                                           int(avg_from[11:13]), int(avg_from[14:16]), int(avg_from[17:19]))

# Retrieve average to
if len(data_PL['streamers'][0]) != 0:
    avg_to = average_viewers_PL['TimeFinished']
    avg_to_formatted_PL = datetime.datetime(int(avg_to[6:10]), int(avg_to[3:5]), int(avg_to[0:2]),
                                         int(avg_to[11:13]), int(avg_to[14:16]), int(avg_to[17:19]))

###########################################################################################################

# Populate average viewers table for english streamers
for streamer in streamers_names_formatted_EN:

    # Retrieve streamer ID
    retrieve_streamer_id_en = "SELECT ID_en FROM streamer_en WHERE name = '" + streamer + "'"
    cursor.execute(retrieve_streamer_id_en)
    id = cursor.fetchall()

    # Retrieve average viewers
    avg_viewers = average_viewers_EN[streamer]

    # Checking if streamer exists in the table
    check_if_exists = "SELECT EXISTS(SELECT * FROM avg_viewers_en where streamer_en_id = '" + str(id[0][0]) + "')"
    cursor.execute(check_if_exists)
    boolean = cursor.fetchall()

    # Checking if the avg_from changed
    check_if_avg_from_changed = "SELECT * FROM avg_viewers_en where streamer_en_id = '" + str(id[0][0]) + "'"
    cursor.execute(check_if_avg_from_changed)
    old_avg_from = cursor.fetchall()

    if len(old_avg_from) != 0:
        if old_avg_from[0][3] != avg_from_formatted_EN:
            update = f"""UPDATE avg_viewers_en
                        SET AVG_VIEWERS = '{average_viewers_EN[streamer]}', 
                        AVG_FROM = '{avg_from_formatted_EN}', AVG_TO = '{avg_to_formatted_EN}'
                        WHERE streamer_en_id = '{id[0][0]}';"""
            cursor.execute(update)

            print("Weszlo")

    # Create table consisting of tuples, which will be added to the database.
    # If the streamer exists in the table he will not be added.
    if boolean[0][0] == 0:
        avgViewersEN.append((id[0][0], avg_viewers, avg_from_formatted_EN, avg_to_formatted_EN))

###########################################################################################################

# Populate average viewers table for polish streamers
for streamer in streamers_names_formatted_PL:

    # Retrieve streamer ID
    retrieve_streamer_id_pl = "SELECT ID_pl FROM streamer_pl WHERE name = '" + streamer + "'"
    cursor.execute(retrieve_streamer_id_pl)
    id = cursor.fetchall()

    # Retrieve average viewers
    avg_viewers = average_viewers_PL[streamer]

    # Checking if streamer exists in the table
    check_if_exists = "SELECT EXISTS(SELECT * FROM avg_viewers_pl where streamer_pl_id = '" + str(id[0][0]) + "')"
    cursor.execute(check_if_exists)
    boolean = cursor.fetchall()

    # Checking if the avg_from changed
    check_if_avg_from_changed = "SELECT * FROM avg_viewers_pl where streamer_pl_id = '" + str(id[0][0]) + "'"
    cursor.execute(check_if_avg_from_changed)
    old_avg_from = cursor.fetchall()

    if len(old_avg_from) != 0:
        if old_avg_from[0][3] != avg_from_formatted_PL:
            update = f"""UPDATE avg_viewers_pl
                            SET AVG_VIEWERS = '{average_viewers_PL[streamer]}', 
                            AVG_FROM = '{avg_from_formatted_PL}', AVG_TO = '{avg_to_formatted_PL}'
                            WHERE streamer_pl_id = '{id[0][0]}';"""
            cursor.execute(update)

            print("Weszlo")

    # Create table consisting of tuples, which will be added to the database
    # If the streamer exists in the table he will not be added.
    if boolean[0][0] == 0:
        avgViewersPL.append((id[0][0], avg_viewers, avg_from_formatted_PL, avg_to_formatted_PL))

# Queries
addAvgViewersEN = 'INSERT INTO avg_viewers_en (STREAMER_EN_ID, AVG_VIEWERS, AVG_FROM, AVG_TO) VALUES (%s, %s, %s, %s)'
addAvgViewersPL = 'INSERT INTO avg_viewers_pl (STREAMER_PL_ID, AVG_VIEWERS, AVG_FROM, AVG_TO) VALUES (%s, %s, %s, %s)'

# Inserting data
cursor.executemany(addAvgViewersEN, avgViewersEN)
cursor.executemany(addAvgViewersPL, avgViewersPL)

# Close connection
connection.commit()
connection.close()

