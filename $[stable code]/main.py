'''

'''
from __imports__ import *
from Harvester import *
from NPCExplorer import auto_explore
# time.sleep(2)
# cityBuilderCommand=os.system('start cmd /K python ./CityBuilder.py ')


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
		vars:cyclesleep
			its a delay backoff time between successive game
			actions to prevent over loading servers and being banned. if we
			get banned it will auto increment to play more slowly, 
			manual intervention not required.
	'''
	cyclesleep=10
	subcyclesleep=1
	sleep=1
	while True:
		errsignal=0
		'''EXPLORE HARVEST IN SAME CYCLE '''

		print('----------| NPC SEQUENCE START 	   |----------')
		try:
			auto_explore(CITY2,123176,sleep=sleep)
			auto_explore(CITY2,CITY2['sector_root'],sleep=sleep)
			auto_explore(CITY5,127272,				sleep=sleep)# mini explore tiles
			UnitManager.rearm_repair_all_units(CITY2,sleep=sleep)
			UnitManager.rearm_repair_all_units(CITY5,sleep=sleep)
		except Exception as e:
			print(f'MAIN:NPC:ERROR {repr(e)}')
			errsignal=1


		print('----------| HARVESTOR SEQUENCE START|----------')
		highYieldDudiSector=119088
		ADA5SelfSector=127272
		try:
			# custom_harvest(CITY1,highYieldDudiSector,shuffle= 1,sleep= sleep)
			custom_harvest(CITY2,123176,				cleartiles= gen_tiles(125224,3),sleep= sleep)
			custom_harvest(CITY3,highYieldDudiSector,	shuffle= 1,	sleep= sleep)
			custom_harvest(CITY5,ADA5SelfSector,		cleartiles= gen_tiles(127277,4),sleep= sleep)
		except Exception as e:
			print(f'MAIN:HARVESTOR:ERROR {repr(e)}')
			errsignal=1

		# print('----------| Builder SEQUENCE START 	   |----------')
		# CityBuilder.city5_plan()
		# CityBuilder.city4_plan()

		if errsignal:
			print("MAIN:ERROR: ALERT BOSS! we encounter a serious error trying to re-login")
			LoginManager.login()
			cyclesleep+=0.5


		print("MAIN:SLEEP: ",cyclesleep,'seconds','var:sleep',sleep)
		time.sleep(cyclesleep)


#_________________________________________________
#                 (_)                     | |     
#  _ __ ___   __ _ _ _ __     ___ ___   __| | ___ 
# | '_ ` _ \ / _` | | '_ \   / __/ _ \ / _` |/ _ \
# | | | | | | (_| | | | | | | (_| (_) | (_| |  __/
# |_| |_| |_|\__,_|_|_| |_|  \___\___/ \__,_|\___|
#-------------------------------------------------

def function(self):
	pass

if __name__ == '__main__':
	sequential_farming_plan()
	...

