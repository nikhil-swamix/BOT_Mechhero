from mxproxy import mx
import re
import requests
import time

import Defaults
import LoginManager
import MapScanner

def get_all_harvestor_info():
	citypage=LoginManager.get_page_soup(f'http://s1.mechhero.com/City.aspx?cid={CITY["cid"]}')


def get_available_hlsots(CITY):
	city_hlevel=int(re.search(r'\d',citypage.select_one('area[title*="Recycling Workshop"]').attrs['title']).group())

	citypage=LoginManager.get_page_soup(f'http://s1.mechhero.com/MissionList.aspx?tab=harvest&cid={CITY["cid"]}')
	city_hmissions=citypage.select('.content .th').__len__()

	empty_slots=city_hlevel - city_hmissions
	print(f'hslots of city {CITY["cid"]}=={empty_slots}')
	return empty_slots

def get_max_harvestors(CITY):
	page=LoginManager.get_page_soup(f'http://s1.mechhero.com/data.dt?provider=misv&cid={CITY["cid"]}&et=33')
	havailable=int(page.text.split('~')[-1])
	return havailable
	
#----------------------------------
def send_harvestor(CITY:'object',TILE):
	'''
	ARGSDEF:
		CITY: class object from MapScanner
		TILE: class object from MapScanner
	'''
	apiurl=f'http://s1.mechhero.com/Building.aspx?sid={CITY["harvestor_sid"]}&mid={TILE.mid}&q=1'
	postdata={
	"__VIEWSTATE": "rAVhS85W+Y/hn8rCAcUv0N8hD4IRzARgOvKDyrAm44BrR03lZUcNpy/YgpmKxi4KrcmU5vYxGGcJKqd+aUPAUN6v5SLy7BQwFS9SFfR2j+0=",
	"__EVENTTARGET": "ctl00$ctl00$body$content$ctl01",
	"quantity": TILE.data['hcost'],
	"tpid": "0",
	"rcid": CITY['cid'],
	"tx": TILE.coords["x"],
	"ty": TILE.coords["y"],
	"tid": "-1",
	"tcid": "126754",
	"tmv": "-1",
	"tspeed": "120",
	"__VIEWSTATEGENERATOR": "2465F31B",
	"__EVENTARGUMENT": "harvest",
	}

	if TILE.data['hcost']==0:
		print("debris below threshold",TILE.coords)
		return 0
	else:
		resp=LoginManager.post(apiurl,postdata)
		print(f'HARVEST: {TILE.data["hcost"]} -> {TILE.coords}')
		return 1



#----------------------------------

def custom_harvest(CITY,mid,n=8):
	'''
		arg1:input a city object with cid
		arg2:imput a mid from world map
		kwarg=n:length of [bounding box] generated. n=8,tiles=64
		[bounding box]:a discrete square grid, if n increase then expands in +x and -y direction 
	'''
	harvestable_tiles=MapScanner.get_harvestable_tiles(mid,n=n)
	hslots=get_available_hlsots(CITY)
	havailable=	get_max_harvestors(CITY)
	enroute=
	for htile in harvestable_tiles:
		tile=MapScanner.Tile(htile)
		if havailable==0 :
			print('LOG: Need More Harvestors to ',tile.coords)
			break
		elif hslots==0:
			print('LOG: R-workshop Max Missions Limit Reached')
			break
		else:
			if send_harvestor(CITY,MapScanner.Tile(htile)):
				havailable-=tile.data['hcost']
				hslots-=1
		time.sleep(1)


def gapchup_city_harvest(CITY):
	custom_harvest(CITY,CITY['sector_root'],n=8)#hemisquareL

if __name__ == '__main__':
	from Defaults import *
	# send_harvestor(Defaults.CITY1,MapScanner.Tile(126243))
	# custom_harvest(Defaults.CITY1,Defaults.CITY1['sector_south'])

	# x=MapScanner.get_harvestable_tiles(120094)
	while True:
		gapchup_city_harvest(CITY1)
		# custom_harvest(Defaults.CITY1,120599,n=12)#hemisquareL
		# custom_harvest(Defaults.CITY1,120610,n=12)#hemisquareR
		print("sleeping 30s"),time.sleep(60)
