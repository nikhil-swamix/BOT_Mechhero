from __imports__ import *
import NPCExplorer,Harvester,ExchangePost,CityBuilder
import LoginManager

def sequential_farming_plan():
	"""
		desc:
			this function will execute a plan to play the game, 
			you may add CITIES and their associated actions from different 
			modules , in a sequential manner. it runs forever. errors are not 
			raised by default to prevent crashing of code in runtime.
		args:
			none not required
		vars:
			cyclesleep:
				progressive delay for every loop cycle, increase if hitting rate limit.
	"""
	cyclesleep=10
	while True:
		errsignal=0
		try:
			NPCExplorer.plan()
			Harvester.plan()
			CityBuilder.plan()
		except Exception as e:
			pass

		if errsignal:
			print("MAIN:ERROR: ALERT BOSS! we encounter a serious error trying to re-login")
			LoginManager.login()
			cyclesleep+=0.5

		print("MAIN:SLEEP: ",cyclesleep,'seconds')
		time.sleep(cyclesleep)


#_________________________________________________
def func(f): 
	f()

def parallel_multitasking_plan(plans):
	global SUPERPOOL
	c=0
	POOL=Pool(4,initializer=threadinit,initargs=[q])
	while True:
		try:
			Logger.breakpoint('TRACE: Starting workers')
			r=POOL.map_async(func,plans)
			r.get()
			c+=1
			time.sleep(10)


		except Exception as e:
			Logger.error('MAIN:ERROR: repr(e) Retrying all plans !!!',)
			time.sleep(10)


#_________________________________________________
def parallel_cmd_execution():
	autoExploreCommand=os.system('start cmd /K python ./NPCExplorer.py')
	autoHarvestCommand=os.system('start cmd /K python ./Harvester.py')

#_________________________________________________
#                 (_)                     | |     
#  _ __ ___   __ _ _ _ __     ___ ___   __| | ___ 
# | '_ ` _ \ / _` | | '_ \   / __/ _ \ / _` |/ _ \
# | | | | | | (_| | | | | | | (_| (_) | (_| |  __/
# |_| |_| |_|\__,_|_|_| |_|  \___\___/ \__,_|\___|
#-------------------------------------------------

def threadinit(q):
	if not q.empty():
		s=q.get(1)
		time.sleep(s)
		LoginManager.login()
	else:
		return

if __name__ == '__main__':
	from multiprocessing import Process,Pool,Manager,Queue,Lock
	# from concurrent.futures import ProcessPoolExecutor,wait

	plans=[
		NPCExplorer.plan, 
		Harvester.plan, 
		CityBuilder.plan,
		# ExchangePost.plan
		]

	mylock=Lock()
	q=Queue(100)
	[q.put(x) for x in range(4)]

	parallel_multitasking_plan(plans)
	

	# POOL.apply(ExchangePost.round_robin_transfer)

