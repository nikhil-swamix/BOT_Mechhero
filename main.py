
def sequential_farming_plan():
	"""
		desc:
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
	"""
	cyclesleep=10
	while True: #EXPLORE HARVEST IN SAME CYCLE """
		errsignal=0
		try:
			pass
		except Exception as e:
			raise e
		NPCExplorer.plan()
		Harvester.plan()
		CityBuilder.plan()


		if errsignal:
			print("MAIN:ERROR: ALERT BOSS! we encounter a serious error trying to re-login")
			LoginManager.login()
			cyclesleep+=0.5

		print("MAIN:SLEEP: ",cyclesleep,'seconds')
		time.sleep(cyclesleep)


#_________________________________________________
def parallel_multitasking_plan():
	plans=[NPCExplorer.plan, Harvester.plan,CityBuilder.plan]
	c=0
	while True:
		try:
			# POOL.map_async(plans[c % len(plans)])
			promise=POOL.map_async(func,plans)
			promise.wait()
			c+=1
		except Exception as e:
			print('MAIN:ERROR: Retrying our plans !!!',e)
			return

def func(f): f()

#_________________________________________________
def parallel_cmd_execution():
	autoExploreCommand=os.system('start cmd /K python ./NPCExplorer.py ')
	autoHarvestCommand=os.system('start cmd /K python ./Harvester.py ')
#_________________________________________________
#                 (_)                     | |     
#  _ __ ___   __ _ _ _ __     ___ ___   __| | ___ 
# | '_ ` _ \ / _` | | '_ \   / __/ _ \ / _` |/ _ \
# | | | | | | (_| | | | | | | (_| (_) | (_| |  __/
# |_| |_| |_|\__,_|_|_| |_|  \___\___/ \__,_|\___|
#-------------------------------------------------
#NOTES
# RAILFACTORY: ETH2 ,ADA5
# NUCLEAR: BNB4
# CERAMIC PLATING: CAKE3,BNB4,RVN7,XMR6
# FORCEFIELD: ADA5,BTC1,SOL8
# X-2M,MEDIUM TRANSPORT PLATFORM: CAKE3 ,USDT9
# JETPACK: XMR 6

if __name__ == '__main__':
	from __imports__ import *
	from multiprocessing import Process,Pool
	POOL=Pool(3)
	parallel_multitasking_plan()


	"""plans"""
	# sequential_farming_plan()
	# parallel_cmd_execution()
