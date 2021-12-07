import pymysql

connection = pymysql.connect(host="localhost", user="root", passwd="", database="Twitch&Weather")
cursor = connection.cursor()

# queries for inserting values
insert1 = """INSERT INTO twitch_streamer_en(NAME, VIEWER_COUNT, AVG_FROM, AVG_TO) 
             VALUES('xqc', '10533', '9999-12-31 23:59:59', '9999-12-31 23:59:59');"""

TwitchStreamerEN = """CREATE TABLE streamer_en(
                    ID INT(20) PRIMARY KEY AUTO_INCREMENT,
                    GAMES_ID_PL INT(20),
                    FOREIGN KEY(GAMES_ID_PL) REFERENCES games(ID),

                    NAME CHAR(30) NOT NULL,
                    CURRENT_VIEWER_COUNT INT(20),
                    FOLLOWERS INT(20)
                    )"""

TwitchStreamerPL = """CREATE TABLE streamer_pl(
                    ID INT(20) PRIMARY KEY AUTO_INCREMENT,
                    GAMES_ID_PL INT(20),
                    FOREIGN KEY(GAMES_ID_PL) REFERENCES games(ID),

                    NAME CHAR(30) NOT NULL,
                    VIEWER_COUNT INT(20),
                    CURRENT_VIEWER_COUNT INT(20),
                    FOLLOWERS INT(20)
                    )"""

GamesTable = """CREATE TABLE games(
                ID INT(20) PRIMARY KEY AUTO_INCREMENT,
                TITLE CHAR(30) NOT NULL,
                RANK INT(20)
                )"""

AverageViewersEN = """CREATE TABLE avg_viewers_en(
                    ID INT(20) PRIMARY KEY AUTO_INCREMENT,
                    STREAMER_EN_ID INT(20),
                    FOREIGN KEY(STREAMER_EN_ID) REFERENCES streamer_en(ID),
                    
                    AVG_VIEWERS INT (20) NOT NULL,
                    AVG_FROM DATETIME(0),
                    AVG_TO DATETIME(0)
                    )"""

AverageViewersPL = """CREATE TABLE avg_viewers_pl(
                    ID INT(20) PRIMARY KEY AUTO_INCREMENT,
                    STREAMER_PL_ID INT(20),
                    FOREIGN KEY(STREAMER_PL_ID) REFERENCES streamer_pl(ID),
                    
                    AVG_VIEWERS INT (20) NOT NULL,
                    AVG_FROM DATETIME(0),
                    AVG_TO DATETIME(0)
                    )"""

WeatherEN = """CREATE TABLE weather_en(
                ID INT(20) PRIMARY KEY AUTO_INCREMENT,
                AVG_VIEWERS_EN_ID INT(20),
                AVG_VIEWERS_EN_STREAMER_EN_ID INT(20),
                FOREIGN KEY(AVG_VIEWERS_EN_ID) REFERENCES avg_viewers_en(ID),
                FOREIGN KEY(AVG_VIEWERS_EN_STREAMER_EN_ID) REFERENCES avg_viewers_en(STREAMER_EN_ID),
                
                TEMP FLOAT(20) NOT NULL,
                DATETIME DATETIME(0) NOT NULL,
                FEELS_LIKE FLOAT(20),
                PRESSURE INT(20)
                )"""

WeatherPL = """CREATE TABLE weather_pl(
                ID INT(20) PRIMARY KEY AUTO_INCREMENT,
                AVG_VIEWERS_PL_ID INT(20),
                AVG_VIEWERS_PL_STREAMER_PL_ID INT(20),
                FOREIGN KEY(AVG_VIEWERS_PL_ID) REFERENCES avg_viewers_pl(ID),
                FOREIGN KEY(AVG_VIEWERS_PL_STREAMER_PL_ID) REFERENCES avg_viewers_pl(STREAMER_PL_ID),
                
                TEMP FLOAT(20) NOT NULL,
                DATETIME DATETIME(0) NOT NULL,
                FEELS_LIKE FLOAT(20),
                PRESSURE INT(20)
                )"""

cursor.execute(TwitchStreamerEN)
cursor.execute(TwitchStreamerPL)
cursor.execute(AverageViewersEN)
cursor.execute(AverageViewersPL)
cursor.execute(GamesTable)
cursor.execute(WeatherEN)
cursor.execute(WeatherPL)
#cursor.execute(insert1)

connection.commit()
connection.close()
