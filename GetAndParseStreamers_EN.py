import requests
import json
import time
from datetime import datetime
import signal
import sys
from threading import *

def handler(signum, frame):
    res = input("Ctrl-c was pressed. The current size of a table with viewiership data is " + str(len(data_over_time['streamers'])) + ". Do you want to save the data to a json file? y/n")
    
    if res == 'y':
    	# Dumping the dictionary as a json file
    	with open('streamers_EN.json', 'w') as f:
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
    'Authorization': 'Bearer 9n6j9z9e1zx3g1jc8ajdguya24y88s',
    'Client-Id': 'v8dly98x0oe9wdmyvgqo3el4s5g12p',
}

params = (
    ('user_login', ['xqcow', 'trainwreckstv', 'lirik', 'loltyler1', 'sodapoppin', 'shroud', 'pokimane', 'fextralife', 'summit1g', 'forsen']),
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
	# Getting date and time of downloading data
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	
	streamers_dict = {}
	
	# Getting data from API
	response = requests.get(URL, headers=headers, params=params).json()

	# Formatting data
	for streamer in response['data']:
		streamers_dict['Time'] = dt_string
		streamers_dict[streamer['user_name']] = streamer['viewer_count']

	# Appending the streamers_dict dictionary to a bigger one - data_over_time
	data_over_time['streamers'].append(streamers_dict)