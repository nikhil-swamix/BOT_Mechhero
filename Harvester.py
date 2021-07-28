from mxproxy import mx
import re
import requests
import time

import Defaults
import LoginManager
import MapScanner

def get_all_harvestor_info(CITY):
	citypage=LoginManager.get_page_soup(f'http://s1.mechhero.com/City.aspx?cid={CITY["cid"]}')
	harvestTabPage=LoginManager.get_page_soup(f'http://s1.mechhero.com/MissionList.aspx?tab=harvest&cid={CITY["cid"]}')
	missionDataAJAX=LoginManager.get_page_soup(f'http://s1.mechhero.com/data.dt?provider=misv&cid={CITY["cid"]}&et=33')

	city_hlevel=int(re.search(r'\d',citypage.select_one('area[title*="Recycling Workshop"]').attrs['title']).group())
	city_hmissions=harvestTabPage.select('.content .th').__len__()
	hslots=city_hlevel - city_hmissions
	havailable=int(missionDataAJAX.text.split('~')[-1])

	enroutes=harvestTabPage.select('tr.th .green')
	enroutes=[x.parent.parent.find_next_sibling().select_one('td:nth-child(2)').text for x in enroutes]
	enroutes=[eval(re.search(r'\(\d.+\d\)',x).group()) for x in enroutes]

	print(f'INFO: city {CITY["cid"]} has [{hslots}] hslots available')
	return {
		'hslots':hslots,
		'havailable':havailable,
		'enroutes':enroutes
		}


	
#----------------------------------
def send_harvestor(CITY:'object',TILE):
	'''
	ARGSDEF:
		CITY: class object from MapScanner
		TILE: class object from MapScanner
	'''
	global havailable
	apiurl=f'http://s1.mechhero.com/Building.aspx?sid={CITY["harvestor_sid"]}&mid={TILE.mid}&q=1'
	postdata={
	"__VIEWSTATE": "rAVhS85W+Y/hn8rCAcUv0N8hD4IRzARgOvKDyrAm44BrR03lZUcNpy/YgpmKxi4KrcmU5vYxGGcJKqd+aUPAUN6v5SLy7BQwFS9SFfR2j+0=",
	"__EVENTTARGET": "ctl00$ctl00$body$content$ctl01",
	"quantity": TILE.data['hcost'],
	"rcid": CITY['cid'],
	"tx": TILE.coords[0], "ty": TILE.coords[1],
	"tpid": "0", "tid": "-1", "tcid": "126754", "tmv": "-1", "tspeed": "120",
	"__VIEWSTATEGENERATOR": "2465F31B",
	"__EVENTARGUMENT": "harvest",
	}

	if TILE.data['hcost']==0:
		print("debris below threshold",TILE.coords)
		return 'require more'

	if TILE.data['hcost']>=havailable:
		postdata.update({"quantity":havailable})
		havailable=0

	resp=LoginManager.post(apiurl,postdata)
	havailable-=min(TILE.data['hcost'],havailable)
	print(f'HARVEST: {TILE.data["hcost"]} -> {TILE.coords} -> havailable[{havailable}]')
	return 'success'



#----------------------------------
def custom_harvest(CITY,mid,n=8,clearence=1):
	'''
		arg1:CITY a city object with cid and other
		arg2:mid a mid from world map
		kwarg=n:length of [bounding box] generated. n=8,tiles=64
		[bounding box]:a discrete square grid, if n increase then expands in +x and -y direction 
		var:htiles = its assured that htiles are only harvestable tiles since we already filtered it
	'''
	global havailable,hslots
	htiles=MapScanner.get_harvestable_tiles(mid,n=n)

	fullData=get_all_harvestor_info(CITY)
	hslots=fullData['hslots']
	havailable=	fullData['havailable']
	clearence=MapScanner.gen_tiles(CITY['cid']-(clearence*513),n=clearence*2+1)
	for htile in htiles:
		TILE=MapScanner.Tile(htile)

		if TILE.mid in clearence:
			TILE.data['hcost']+=1
			print('CLEARING TILE NIGGA! ',TILE.coords)

		if TILE.coords in fullData['enroutes']:
			print('WARN: redundant mission, Skipping')
			continue

		if havailable==0 :
			print('FAIL: NEED MORE HARVESTERS to ',TILE.coords)
			break

		if hslots==0:
			print('FAIL: R-WORKSHOP MAX MISSIONS LIMIT REACHED')
			break
		
		state=send_harvestor(CITY,TILE)
		if state=='success':
			hslots-=1
		time.sleep(1)


def gapchup_city_harvest(CITY):
	custom_harvest(CITY,CITY['sector_root'],n=8,clearence=1)#hemisquareL




if __name__ == '__main__':
	from Defaults import *
	highYieldSector=119080
	# send_harvestor(Defaults.CITY1,MapScanner.Tile(126243))
	# get_all_harvestor_info(CITY1)

	# custom_harvest(Defaults.CITY1,highYieldSector)
	# gapchup_city_harvest(CITY1)
	while True:
		custom_harvest(Defaults.CITY1,Defaults.CITY1['sector_root'])#hemisquareL
		custom_harvest(Defaults.CITY2,highYieldSector)#hemisquareL
		# custom_harvest(Defaults.CITY1,120610,n=12)#hemisquareR
		print("sleeping 120s"),time.sleep(120)

