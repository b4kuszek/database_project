import requests
import json
import time
import signal
import sys
import pytz
from threading import *
from datetime import datetime

def handler(signum, frame):
    res = input("Ctrl-c was pressed. The current size of a table with viewiership data is " + str(len(data_over_time['streamers'])) + ". Do you want to save the data to a json file? y/n")
    
    if res == 'y':
        # Dumping the dictionary as a json file
        with open('streamers_PL.json', 'w') as f:
            json.dump(data_over_time, f)
            
        f.close()
        sys.exit(0)

# Creating class which manages threads
class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(1):
            GetData()
            print("The current size of a table with viewiership data is: " + str(len(data_over_time['streamers'])))
            
###################################################################

URL = 'https://api.twitch.tv/helix/streams'

headers = {
    'Authorization': 'Bearer xnzpq6d45ptdy4ul5egcr2mmy9wk21',
    'Client-Id': 'v8dly98x0oe9wdmyvgqo3el4s5g12p',
}

params = (
    ('user_login', ['overpow', 'ewroon', 'popo', 'nervarien', 'vysotzky', 'pago3', 'izakooo', 'RybsonLoL_', 'polsatgames', 'xth0rek']),
)

# Creating a dictionary which will contain streamer names and their viewer counts over time
data_over_time = {}
data_over_time['streamers'] = []

# Creating a CTR+C exception handler
signal.signal(signal.SIGINT, handler)

# Starting a thread which runs the GetData() function
print("Gathering data...")
stopFlag = Event()
thread = MyThread(stopFlag)
thread.start()


###################################################################
    
def GetData():
    # Getting date and time of downloading data (with correct timezone)
    tz_WWA = pytz.timezone('Europe/Warsaw')
    datetime_WWA = datetime.now(tz_WWA)
    dt_string = datetime_WWA.strftime("%d/%m/%Y %H:%M:%S")
    
    streamers_dict = {}
    
    # Getting data from API
    response = requests.get(URL, headers=headers, params=params).json()

    # Formatting data
    for streamer in response['data']:
        streamers_dict['Time'] = dt_string
        streamers_dict[streamer['user_name']] = streamer['viewer_count']

    # Appending the streamers_dict dictionary to a bigger one - data_over_time
    data_over_time['streamers'].append(streamers_dict)