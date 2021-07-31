from __init__ import *

# time.sleep(2)
# cityBuilderCommand=os.system('start cmd /K python ./CityBuilder.py ')
# time.sleep(2)
# autoExploreCommand=os.system('start cmd /K python ./NPCExplorer.py ')
# time.sleep(2)
# autoHarvestCommand=os.system('start cmd /K python ./Harvester.py ')

def sequential_farming_plan():
	'''
		desc>
			this function will execute a plan to play the game, 
			you may add CITIES and their associated actions from different 
			modules , in a sequential manner. it runs forever. errors are not 
			raised by default to prevent crashing of code in runtime.
		args:none 
			not required everything is defined inside, raise errors to check
		vars:progbackoff
			its a delay backoff time between successive game
			actions to prevent over loading servers and being banned. if we
			get banned it will auto increment to play more slowly, 
			manual intervention not required.
	'''
	LoginManager.auto_login()
	progbackoff=20
	progfactor=1
	while True:
		'''EXPLORE HARVEST IN SAME CYCLE '''
		try:
			print('*********************| NPC SEQUENCE STARTED |*********************')
			UnitManager.rearm_repair_all_units(CITY2,sleep=progbackoff/10)
			NPCExplorer.auto_explore(CITY2,CITY2['sector_east'],sleep=progbackoff/10)
			NPCExplorer.auto_explore(CITY2,CITY2['sector_root'],sleep=progbackoff/10)

			print('*********************| HARVESTOR SEQUENCE STARTED |*********************-')
			Harvester.custom_harvest(CITY2,CITY2['sector_east'],shuffle=0,reverse=1,sleep=progbackoff/10)
			Harvester.custom_harvest(CITY1,CITY1['sector_root'],shuffle=1,sleep=progbackoff/10)

			print('*********************| BUILDER SEQUENCE STARTED |*********************-')
			# CityBuilder.city3plan()

		except Exception as e:
			# raise e
			print(f'MAIN:ERROR: {repr(e)} EXCEEDING API LIMIT! SLEEP FOR',progbackoff)
			print(f'MAIN:ERROR: REDUCING SPEED by progfactor to avoid API LIMIT! sleep',progbackoff,'s')
			progbackoff+=progfactor
			time.sleep(progbackoff)
			LoginManager.auto_login()

		print("MAIN:SLEEP: zzzzz",progbackoff,'seconds')
		time.sleep(progbackoff)


#_________________________________________________
#                 (_)                     | |     
#  _ __ ___   __ _ _ _ __     ___ ___   __| | ___ 
# | '_ ` _ \ / _` | | '_ \   / __/ _ \ / _` |/ _ \
# | | | | | | (_| | | | | | | (_| (_) | (_| |  __/
# |_| |_| |_|\__,_|_|_| |_|  \___\___/ \__,_|\___|
#-------------------------------------------------
sequential_farming_plan()