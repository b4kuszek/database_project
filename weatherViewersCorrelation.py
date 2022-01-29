import pymysql
import json
import requests
import datetime

# Connecting to DB
connection = pymysql.connect(host="localhost", user="root", passwd="", database="Twitch&Weather")
cursor = connection.cursor()

###############################################################################
# Retrieve ID_pl from streamer_pl table
retrieve_PL = "SELECT * FROM streamer_pl"
cursor.execute(retrieve_PL)
rows_PL = cursor.fetchall()

# Retrieve ID_en from streamer_en table
retrieve_EN = "SELECT * FROM streamer_en"
cursor.execute(retrieve_EN)
rows_EN = cursor.fetchall()

# Create table of streamers names from streamer_pl
streamers_in_streamer_pl = []
for streamer in rows_PL:
    streamers_in_streamer_pl.append(streamer[1])

# Create table of streamers names from streamer_en
streamers_in_streamer_en = []
for streamer in rows_EN:
    streamers_in_streamer_en.append(streamer[1])

###############################################################################
Weather_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Creating empty weather tables
weather_pl = []
weather_en = []

# Creating dictionary of POLISH streamers - streamers_name : city
cities_PL = {}
cities_PL['Overpow'] = 'Poznan'; cities_PL['EWROON'] = 'Warszawa'; cities_PL['popo'] = 'Mielec';
cities_PL['Nervarien'] = 'Krakow'; cities_PL['vysotzky'] = 'Mielec'; cities_PL['PAGO3'] = 'Krakow';
cities_PL['IzakOOO'] = 'Warszawa'; cities_PL['RybsonLoL_'] = 'Katowice'; cities_PL['polsatgames'] = 'Warszawa';
cities_PL['xth0rek'] = 'London'

# Creating dictionary of ENGLISH streamers - streamers_name : city
cities_EN = {}
cities_EN['xQcOW'] = 'Texas'; cities_EN['Trainwreckstv'] = 'Ottawa'; cities_EN['LIRIK'] = 'Los Angeles';
cities_EN['loltyler1'] = 'Fayette'; cities_EN['sodapoppin'] = 'Texas'; cities_EN['shroud'] = 'Mississauga';
cities_EN['pokimane'] = 'Ottawa'; cities_EN['Fextralife'] = 'Atlanta'; cities_EN['summit1g'] = 'Colorado';
cities_EN['forsen'] = 'Umea'

# Table of streamers names from cities_PL dictionary
streamers_list_from_cities_PL = list(cities_PL.keys())

# Table of streamers names from cities_EN dictionary
streamers_list_from_cities_EN = list(cities_EN.keys())

###############################################################################

# Creating weather_pl table of tuples
for streamer in streamers_in_streamer_pl:
    if streamer in streamers_list_from_cities_PL:
        Weather_response_PL = requests.get(
            Weather_URL,
            params={'q': cities_PL[streamer], 'appid': 'd9c4a372c76d3499d793a682f4c4b21d'}
        ).json()

        # Getting info from response
        GeneralWeatherInfo = Weather_response_PL['weather'][0]['main']
        SpecificWeatherInfo = Weather_response_PL['main']

        City = Weather_response_PL['name']
        Temperature = SpecificWeatherInfo['temp'] - 273.15  # conversion to Celsius
        FeelsLike = SpecificWeatherInfo['feels_like'] - 273.15  # conversion to Celsius
        Pressure = SpecificWeatherInfo['pressure']

        # Retrieve id based on streamers name from streamer_pl table
        streamer_pl_id = "SELECT ID_pl FROM streamer_pl WHERE name = '" + streamer + "'"
        cursor.execute(streamer_pl_id)
        streamer_pl_id_fetch = cursor.fetchall()
        streamer_pl_id_fetch_formatted = streamer_pl_id_fetch[0][0]

        # Retrieve avg_viewers_pl id based on streamer_pl id from avg_viewers_pl table
        avg_viewers_pl_id = "SELECT ID FROM avg_viewers_pl WHERE streamer_pl_id = " + str(streamer_pl_id_fetch[0][0])
        cursor.execute(avg_viewers_pl_id)
        avg_viewers_pl_id_fetch = cursor.fetchall()
        avg_viewers_pl_id_fetch_formatted = avg_viewers_pl_id_fetch[0][0]

        # Defining datetime
        Datetime = datetime.datetime.now()

        # Checking if weather data for streamer already exists in the database
        check_if_exists = "SELECT EXISTS(SELECT * FROM weather_pl where avg_viewers_pl_streamer_pl_id = '" \
                          + str(streamer_pl_id_fetch_formatted) + "')"

        cursor.execute(check_if_exists)
        boolean = cursor.fetchall()
        boolean_formatted = boolean[0][0]

        # Checking if the value for general info have changed
        if boolean_formatted == 1:
            check_if_changed = "SELECT general_info FROM weather_pl"
            cursor.execute(check_if_changed)
            general_info = cursor.fetchall()[0][0]

            if general_info != GeneralWeatherInfo:
                update = f"""UPDATE weather_pl
                                SET general_info = '{GeneralWeatherInfo}'
                                WHERE general_info = '{general_info}';"""
                cursor.execute(update)

        # Append the data to weather_pl table if it doesn't exist
        if boolean_formatted == 0:
            # Appending tuple to weather_pl table
            weather_pl.append((avg_viewers_pl_id_fetch_formatted, streamer_pl_id_fetch_formatted,
                               City, GeneralWeatherInfo, Temperature, Datetime, FeelsLike, Pressure))

###############################################################################

# Creating weather_en table of tuples
for streamer in streamers_in_streamer_en:
    if streamer in streamers_list_from_cities_EN:
        Weather_response_EN = requests.get(
            Weather_URL,
            params={'q': cities_EN[streamer], 'appid': 'd9c4a372c76d3499d793a682f4c4b21d'}
        ).json()

        # Getting info from response
        GeneralWeatherInfo = Weather_response_EN['weather'][0]['main']
        SpecificWeatherInfo = Weather_response_EN['main']

        City = Weather_response_EN['name']
        Temperature = SpecificWeatherInfo['temp'] - 273.15  # conversion to Celsius
        FeelsLike = SpecificWeatherInfo['feels_like'] - 273.15  # conversion to Celsius
        Pressure = SpecificWeatherInfo['pressure']

        # Retrieve id based on streamers name from streamer_pl table
        streamer_en_id = "SELECT ID_en FROM streamer_en WHERE name = '" + streamer + "'"
        cursor.execute(streamer_en_id)
        streamer_en_id_fetch = cursor.fetchall()
        streamer_en_id_fetch_formatted = streamer_en_id_fetch[0][0]

        # Retrieve avg_viewers_pl id based on streamer_pl id from avg_viewers_pl table
        avg_viewers_en_id = "SELECT ID FROM avg_viewers_en WHERE streamer_en_id = " + str(streamer_en_id_fetch[0][0])
        cursor.execute(avg_viewers_en_id)
        avg_viewers_en_id_fetch = cursor.fetchall()
        avg_viewers_en_id_fetch_formatted = avg_viewers_en_id_fetch[0][0]

        # Defining datetime
        Datetime = datetime.datetime.now()

        # Checking if weather data for streamer already exists in the database
        check_if_exists = "SELECT EXISTS(SELECT * FROM weather_en where avg_viewers_en_streamer_en_id = '" \
                          + str(streamer_en_id_fetch_formatted) + "')"
        cursor.execute(check_if_exists)
        boolean = cursor.fetchall()
        boolean_formatted = boolean[0][0]

        # Checking if the value for general info have changed
        if boolean_formatted == 1:
            check_if_changed = "SELECT general_info FROM weather_en"
            cursor.execute(check_if_changed)
            general_info = cursor.fetchall()[0][0]

            if general_info != GeneralWeatherInfo:
                update = f"""UPDATE weather_en
                                SET general_info = '{GeneralWeatherInfo}'
                                WHERE general_info = '{general_info}';"""
                cursor.execute(update)

        # Append the data to weather_pl table if it doesn't exist
        if boolean_formatted == 0:
            # Appending tuple to weather_pl table
            weather_en.append((avg_viewers_en_id_fetch_formatted, streamer_en_id_fetch_formatted,
                               City, GeneralWeatherInfo, Temperature, Datetime, FeelsLike, Pressure))

###############################################################################
# Queries
addWeatherPL = 'INSERT INTO weather_pl' \
               '(AVG_VIEWERS_PL_ID, AVG_VIEWERS_PL_STREAMER_PL_ID, CITY, ' \
               'GENERAL_INFO, TEMP, DATETIME, FEELS_LIKE, PRESSURE)' \
               'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

addWeatherEN = 'INSERT INTO weather_en' \
               '(AVG_VIEWERS_EN_ID, AVG_VIEWERS_EN_STREAMER_EN_ID, CITY, ' \
               'GENERAL_INFO, TEMP, DATETIME, FEELS_LIKE, PRESSURE)' \
               'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

# Inserting data
cursor.executemany(addWeatherPL, weather_pl)
cursor.executemany(addWeatherEN, weather_en)

###############################################################################
# Close connection
connection.commit()
connection.close()