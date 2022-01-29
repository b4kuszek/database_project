import pymysql

# Connecting to DB
connection = pymysql.connect(host="localhost", user="root", passwd="", database="Twitch&Weather")
cursor = connection.cursor()

# Creating queries
TwitchStreamerEN = """CREATE TABLE streamer_en(
                    ID_en INT(20) PRIMARY KEY AUTO_INCREMENT,
                    NAME CHAR(30) NOT NULL,
                    GAME_ID INT(20),
                    CURRENT_TWITCH_GAME_ID INT(20),
                    FOREIGN KEY (GAME_ID) REFERENCES games(ID)
                    )"""

TwitchStreamerPL = """CREATE TABLE streamer_pl(
                    ID_pl INT(20) PRIMARY KEY AUTO_INCREMENT,
                    NAME CHAR(30) NOT NULL,
                    GAME_ID INT(20),
                    CURRENT_TWITCH_GAME_ID INT(20),
                    FOREIGN KEY (GAME_ID) REFERENCES games(ID)
                    )"""

GamesTable = """CREATE TABLE games(
                ID INT(20) PRIMARY KEY AUTO_INCREMENT,
                TITLE CHAR(30) NOT NULL,
                TWITCH_GAME_ID INT(20)
                )"""

AverageViewersEN = """CREATE TABLE avg_viewers_en(
                    ID INT(20) PRIMARY KEY AUTO_INCREMENT,
                    STREAMER_EN_ID INT(20),
                    FOREIGN KEY (STREAMER_EN_ID) REFERENCES streamer_en(ID_en),
                    AVG_VIEWERS INT (20) NOT NULL,
                    AVG_FROM DATETIME(0),
                    AVG_TO DATETIME(0),
                    UNIQUE (STREAMER_EN_ID)
                    )"""

AverageViewersPL = """CREATE TABLE avg_viewers_pl(
                    ID INT(20) PRIMARY KEY AUTO_INCREMENT,
                    STREAMER_PL_ID INT(20),
                    FOREIGN KEY (STREAMER_PL_ID) REFERENCES streamer_pl(ID_pl),
                    AVG_VIEWERS INT (20) NOT NULL,
                    AVG_FROM DATETIME(0),
                    AVG_TO DATETIME(0),
                    UNIQUE (STREAMER_PL_ID)
                    )"""

WeatherEN = """CREATE TABLE weather_en(
                ID INT(20) PRIMARY KEY AUTO_INCREMENT,
                AVG_VIEWERS_EN_ID INT(20),
                AVG_VIEWERS_EN_STREAMER_EN_ID INT(20),
                FOREIGN KEY(AVG_VIEWERS_EN_ID) REFERENCES avg_viewers_en(ID),
                FOREIGN KEY(AVG_VIEWERS_EN_STREAMER_EN_ID) REFERENCES avg_viewers_en(STREAMER_EN_ID),
                UNIQUE(AVG_VIEWERS_EN_ID, AVG_VIEWERS_EN_STREAMER_EN_ID),
                CITY CHAR(20),
                GENERAL_INFO CHAR(20),
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
                UNIQUE(AVG_VIEWERS_PL_ID, AVG_VIEWERS_PL_STREAMER_PL_ID),
                CITY CHAR(20),
                GENERAL_INFO CHAR(20),
                TEMP FLOAT(20) NOT NULL,
                DATETIME DATETIME(0) NOT NULL,
                FEELS_LIKE FLOAT(20),
                PRESSURE INT(20)
                )"""

DropTables = """DROP TABLE `avg_viewers_en`, `avg_viewers_pl`, `games`, `streamer_en`, `streamer_pl`, `weather_en`, 
                `weather_pl`; """

# Delete tables
#cursor.execute(DropTables)

# Creating tables
cursor.execute(GamesTable)
cursor.execute(TwitchStreamerEN)
cursor.execute(TwitchStreamerPL)
cursor.execute(AverageViewersEN)
cursor.execute(AverageViewersPL)
cursor.execute(WeatherEN)
cursor.execute(WeatherPL)

# Closing the connection
connection.commit()
connection.close()