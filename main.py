from __imports__ import *

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
		vars:progsleep
			its a delay backoff time between successive game
			actions to prevent over loading servers and being banned. if we
			get banned it will auto increment to play more slowly, 
			manual intervention not required.
	'''
	LoginManager.auto_login()
	progsleep=20
	progfactor=2
	while True:
		sleep=progsleep/10
		'''EXPLORE HARVEST IN SAME CYCLE '''
		try:
	
			print('----------| NPC SEQUENCE START 	   |----------')
			NPCExplorer.plan1(sleep)

			print('----------| HARVESTOR SEQUENCE START|----------')
			Harvester.plan1(sleep)

		except Exception as e:
			progsleep*=progfactor
			print('MAIN:ERROR:',repr(e))
			LoginManager.auto_login()
			# raise e

		progsleep-=1
		print("MAIN:SLEEP: ",progsleep,'seconds')
		time.sleep(progsleep)


#_________________________________________________
#                 (_)                     | |     
#  _ __ ___   __ _ _ _ __     ___ ___   __| | ___ 
# | '_ ` _ \ / _` | | '_ \   / __/ _ \ / _` |/ _ \
# | | | | | | (_| | | | | | | (_| (_) | (_| |  __/
# |_| |_| |_|\__,_|_|_| |_|  \___\___/ \__,_|\___|
#-------------------------------------------------
if __name__ == '__main__':
	sequential_farming_plan()