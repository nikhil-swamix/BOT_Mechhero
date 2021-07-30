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
			everything is defined inside, raise errors to check
		vars:progbackoff
			its a delay backoff time between successive game
			actions to prevent over loading servers and being banned. if we
			get banned it will auto increment to play more slowly, 
			manual intervention not required.
	'''
	LoginManager.auto_login()
	progbackoff=10
	progfactor=1
	while True:
		'''EXPLORE HARVEST IN SAME CYCLE '''
		try:
			UnitManager.rearm_repair_all_units(CITY2,sleep=progbackoff/10)
			NPCExplorer.auto_explore(CITY2,CITY2['sector_east'],sleep=progbackoff/10)
			NPCExplorer.auto_explore(CITY2,CITY2['sector_root'],sleep=progbackoff/10)
			Harvester.custom_harvest(CITY2,CITY2['sector_east'],shuffle=0,reverse=1,sleep=progbackoff/10)
			Harvester.custom_harvest(CITY1,CITY2['sector_east'],shuffle=1,sleep=progbackoff/10)
			CityBuilder.city3plan()
		except Exception as e:
			print(f'MAIN:ERROR: {repr(e)} EXCEEDING API LIMIT! SLEEP FOR',progbackoff)
			print(f'MAIN:ERROR: REDUCING SPEED by progfactor to avoid API LIMIT! sleep',progbackoff,'s')
			progbackoff+=progfactor
			time.sleep(progbackoff)
			LoginManager.login()

		print("MAIN:SLEEP: zzzzz",)
		time.sleep(progbackoff)


#______________________________________START
sequential_farming_plan()