from mxproxy import mx
import re
import requests
import time

from __imports__ import *
from MapScanner import gen_tiles,get_harvestable_tiles,Tile


#----------------------------------
def send_harvestor(CITY,TILE):
	'''
		arg:CITY> class object from MapScanner
		arg:TILE> class object from MapScanner
	'''
	global havailable,hslots
	apiurl= f'http://s1.mechhero.com/Building.aspx?sid={CITY["harvestor_sid"][0]}&mid={TILE.mid}&q= 2'
	postdata={
	"__VIEWSTATE": "rAVhS85W+Y/hn8rCAcUv0N8hD4IRzARgOvKDyrAm44BrR03lZUcNpy/YgpmKxi4KrcmU5vYxGGcJKqd+aUPAUN6v5SLy7BQwFS9SFfR2j+0=",
	"__EVENTTARGET": "ctl00$ctl00$body$content$ctl01",
	"quantity": min(TILE.data['hcost'],havailable),
	"rcid": CITY['cid'],
	"tx": TILE.coords[0], "ty": TILE.coords[1],
	"tpid": "0", "tid": "-1", "tcid": CITY['cid'], "tmv": "-1", "tspeed": "12",
	"__VIEWSTATEGENERATOR": "2465F31B",
	"__EVENTARGUMENT": "harvest",
	}

	if TILE.data['hcost']>=havailable:
		postdata.update({"quantity":havailable})
		havailable= 0

	resp= LoginManager.post(apiurl,postdata,)
	havailable -= min(TILE.data['hcost'],havailable)
	hslots -= 1
	Logger.success(f'HARVEST:SENDING: hcost:{TILE.data["hcost"]}->{TILE.coords} |havailable:{havailable}|hslots:{hslots}')
	return 'success'


#----------------------------------
def auto_harvest(CITY, mid, n= 8, htiles=[], cleartiles=[], clearadius= 1, shuffle= 0, reverse= 0,
	sleep= 0.5, debug= 0):
	'''
		arg1:CITY a city object with cid and other
		arg2:mid a mid from world map
		kwarg= n:length of [bounding box] generated. n= 8,tiles= 64
		[bounding box]:a discrete square grid, if n increase then expands in +x and -y direction 
		var:htiles = its assured that htiles are only harvestable tiles since we already filtered it in mapscanner
		note: first priority is given to clear tiles, and second to other tiles in the sector
	'''
	global havailable,hslots,EXPBACKOFF

	'''DATA intel'''
	cityResourceData=City.get_res_info(CITY)
	fullData= City.get_all_harvestor_info(CITY)
	hslots= fullData['hslots']
	havailable=	fullData['havailable']
	cityNearbyHtiles=[]

	'''Clearence calculation'''
	htiles= get_harvestable_tiles(mid,n= n)
	if clearadius>0:
		cityNearbyHtiles= get_harvestable_tiles(CITY['cid']-(clearadius*513),n= clearadius*2+1)
		cityNearbyHtiles= sorted(list( set(cityNearbyHtiles) & set(htiles) ) ) # logical intersection
	cleartiles= list(set(htiles) & set(cleartiles))
	finalcleartiles= cleartiles + cityNearbyHtiles
	# print(finalcleartiles)
	htiles= finalcleartiles+htiles

	'''ARG MOD PROCESSING'''
	if reverse==1 : htiles.reverse()
	if shuffle==1 : htiles= mx.shuffle(htiles)

	for htile in htiles:
		# print(htile)
		time.sleep(sleep)

		if any(x==0 for x in cityResourceData['deficit']) :
			Logger.warn(f'HARVEST:WARN: [CITY{CITY["name"]}] ALREADY FULL')
			return

		try:
			TILE= Tile(htile)
		except Exception as e:
			print(f'HARVEST:ERROR:Tile Instantiation Failed -',htile,'will attempt login')
			print(TILE.data)
			LoginManager.login()

		if debug:
			print('scanning TILE',htile)

		if TILE.data['hcost']<=2: #minimum send threshold
			continue

		if TILE.mid in finalcleartiles: #clear a tile
			TILE.data['hcost']+=1 

		if TILE.coords in fullData['enroutes']:
			print(f'HARVEST:WARN: redundant mission @{TILE.coords}, Skipping')
			continue

		if not debug:
			result= send_harvestor(CITY,TILE)

		if hslots==0:
			Logger.warn(f'HARVEST:FAIL: R-WORKSHOP MAX MISSIONS LIMIT REACHED')
			break

		if havailable==0 :
			Logger.warn(f'HARVEST:FAIL: NEED MORE HARVESTERS to ',TILE.coords)
			break


	return 'success'

def city_harvest(CITY):
	auto_harvest(CITY,CITY['sector_root'])#hemisquareL


#________________start___________________
#  __  __       ___ __    __  __  __  ___ 
# |  \|__)|\  /|__ |__)  /  `/  \|  \|__  
# |__/|  \| \/ |___|  \  \__,\__/|__/|___ 
#______________drivercode________________
highYieldDudiSector=119088

def plan():
	while True:
		try:
			exec(mx.fread('strategies/harvestplan.py'))
		except Exception as e:
			print(e)
			LoginManager.login()
		time.sleep(10)
		
if __name__ == '__main__':
	city_harvest(CITY1)
	# LoginManager.login()
	# plan()