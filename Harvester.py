from mxproxy import mx
import re
import requests
import time

from __imports__ import *
from MapScanner import gen_tiles,get_harvestable_tiles,Tile

def get_all_harvestor_info(CITY):
	'''
		Self explanatory
	'''
	citypage= LoginManager.get_page_soup(f'http://s1.mechhero.com/City.aspx?cid={CITY["cid"]}')
	harvestTabPage= LoginManager.get_page_soup(f'http://s1.mechhero.com/MissionList.aspx?tab=harvest&cid={CITY["cid"]}')
	missionDataAJAX= LoginManager.get_page_soup(f'http://s1.mechhero.com/data.dt?provider=misv&cid={CITY["cid"]}&et= 33')

	city_hlevel= int(re.search(r'\d+',citypage.select_one('area[title*="Recycling Workshop"]').attrs['title']).group())
	city_hmissions= harvestTabPage.select('.content .th').__len__()
	hslots= city_hlevel - city_hmissions
	havailable= int(missionDataAJAX.text.split('~')[-1])

	enroutes= harvestTabPage.select('tr.th .green')
	enroutes=[x.parent.parent.find_next_sibling().select_one('td:nth-child(2)').text for x in enroutes]
	enroutes=[eval(re.search(r'\(\d.+\d\)',x).group()) for x in enroutes]

	print(f'HARVEST:INFO: city={CITY["name"]} hslots=[{hslots}] harvestors={havailable}')
	return {
		'hslots':hslots,
		'havailable':havailable,
		'enroutes':enroutes
		}
	
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
	"quantity": TILE.data['hcost'],
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
	print(f'HARVEST:SENDING: hcost:{TILE.data["hcost"]}->{TILE.coords} |havailable:{havailable}|hslots:{hslots}')
	return 'success'


#----------------------------------
def auto_harvest(CITY, mid, n= 8, htiles=[], cleartiles=[], clearadius= 2, shuffle= 0, reverse= 0,
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
	fullData= get_all_harvestor_info(CITY)
	hslots= fullData['hslots']
	havailable=	fullData['havailable']

	'''ARG MOD'''
	if reverse==1 : htiles.reverse()
	if shuffle==1 : htiles= mx.shuffle(htiles)

	'''Clearence calculation'''
	htiles= get_harvestable_tiles(mid,n= n) 
	cityNearbyHtiles= get_harvestable_tiles(CITY['cid']-(clearadius*513),n= clearadius*2+1)
	cityNearbyHtiles= sorted(list( set(cityNearbyHtiles) & set(htiles) ) ) # logical intersection
	cleartiles= list(set(htiles) & set(cleartiles))
	finalcleartiles= sorted(list(cleartiles + cityNearbyHtiles))
	# print(finalcleartiles)
	htiles= finalcleartiles+htiles
	for htile in htiles:
		time.sleep(sleep)
		if debug:
			print('scanning TILE',htile)

		try:
			TILE= Tile(htile)
			# assert TILE.data['hcost']
		except Exception as e:
			print(f'HARVEST:ERROR:Tile Instantiation Failed -',htile)
			print(TILE.data)
			return

		if TILE.data['hcost']==0: #minimum send threshold
			continue

		if havailable==0 :
			print(f'HARVEST:FAIL: NEED MORE HARVESTERS to ',TILE.coords)
			break

		if hslots==0:
			print(f'HARVEST:FAIL: R-WORKSHOP MAX MISSIONS LIMIT REACHED')
			break

		if TILE.mid in finalcleartiles: #clear a tile
			TILE.data['hcost']+=2 

		if TILE.coords in fullData['enroutes']:
			print(f'HARVEST:WARN: redundant mission @{TILE.coords}, Skipping')
			continue

		if not debug:
			result= send_harvestor(CITY,TILE)

	return 'success'

def citysector_harvest(CITY):
	auto_harvest(CITY,CITY['sector_root'],n= 8)#hemisquareL


#________________start___________________
#  __  __       ___ __    __  __  __  ___ 
# |  \|__)|\  /|__ |__)  /  `/  \|  \|__  
# |__/|  \| \/ |___|  \  \__,\__/|__/|___ 
#______________drivercode________________
highYieldDudiSector=119088
ADA5_West=127272
ADA5_Root=127280

def plan():
	exec(mx.fread('strategies/harvestplan.py'))

# def plancron(): ##continuous plan exec
# 	while True:
# 		print('----------| HARVESTOR SEQUENCE START|----------')
# 		try:
# 			plan()
# 		except Exception as e:
# 			print(f'HARVESTOR:ERROR {repr(e)}')
# 			LoginManager.login()
# 		time.sleep(10)

if __name__ == '__main__':
	# plan()
	# auto_harvest(CITY3,ADA5_West, cleartiles= gen_tiles(ADA5_Root,3))
	auto_harvest(CITY8,135472, cleartiles=gen_tiles(135472,3) )
