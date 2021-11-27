import json

# DEFINING FUNCTIONS #######################################################################################

def CalcAverageViewers_EN():

	average_viewers = {}
	average_viewers['TimeStarted'] = time_started_EN
	average_viewers['TimeFinished'] = time_finished_EN
	
	for i in range(len(streamers_list_EN)):

		viewers_EN = []
		
		for streamer in data_EN['streamers']:
			viewers_EN.append(streamer[streamers_list_EN[i]])
			
		viewers_sum_EN = sum(viewers_EN)
		viewers_average_EN = viewers_sum_EN/len(viewers_EN)
		
		average_viewers[streamers_list_EN[i]] =  viewers_average_EN
		
	with open('Average_Viewers_EN.json', 'w') as f:
		json.dump(average_viewers, f)
	f.close()
	
def CalcAverageViewers_PL():
	average_viewers = {}
	average_viewers['TimeStarted'] = time_started_PL
	average_viewers['TimeFinished'] = time_finished_PL

	for i in range(len(streamers_list_PL)):

		viewers_PL = []
		
		for streamer in data_PL['streamers']:
			viewers_PL.append(streamer[streamers_list_PL[i]])
			
		viewers_sum_PL = sum(viewers_PL)
		viewers_average_PL = viewers_sum_PL/len(viewers_PL)

		average_viewers[streamers_list_PL[i]] =  viewers_average_PL
	
	with open('Average_Viewers_PL.json', 'w') as f:
		json.dump(average_viewers, f)
	f.close()

# CREATING STREAMERS LISTS ################################################################################

f_EN = open('streamers_EN.json')
f_PL = open('streamers_PL.json')

data_EN = json.load(f_EN)
data_PL = json.load(f_PL)

for streamer in data_EN['streamers']:
	streamers_list_EN = list(streamer.keys())[1:]
	
for streamer in data_PL['streamers']:
	streamers_list_PL = list(streamer.keys())[1:]

time_started_EN = (data_EN['streamers'][0]['Time'])
time_finished_EN = (data_EN['streamers'][-1]['Time'])

time_started_PL = (data_PL['streamers'][0]['Time'])
time_finished_PL = (data_PL['streamers'][-1]['Time'])

# RUNNING FUNCTIONS #######################################################################################

CalcAverageViewers_EN()
CalcAverageViewers_PL()
	
###########################################################################################################
