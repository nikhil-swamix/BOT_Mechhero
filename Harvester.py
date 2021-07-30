from mxproxy import mx
import re
import requests
import time

import LoginManager
import MapScanner
import NPCExplorer
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

	print(f'HARVEST:INFO: city={CITY["cid"]} hslots=[{hslots}] harvestors={havailable}')
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
	apiurl=f'http://s1.mechhero.com/Building.aspx?sid={CITY["harvestor_sid"]}&mid={TILE.mid}&q=4'
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

	if TILE.data['hcost']==0:
		# print("No 🚩",TILE.coords)
		return 'below threshold'

	if TILE.data['hcost']>=havailable:
		postdata.update({"quantity":havailable})
		havailable=0

	resp=LoginManager.post(apiurl,postdata)
	hslots-=1
	havailable-=min(TILE.data['hcost'],havailable)
	print(f'HARVEST:SEND: hcost:{TILE.data["hcost"]}->{TILE.coords} |havailable:{havailable}|hslots:{hslots}')
	return 'success'


#----------------------------------
def custom_harvest(CITY,mid,n=8,clearence=2,shuffle=0,reverse=0,sleep=1):
	'''
		arg1:CITY a city object with cid and other
		arg2:mid a mid from world map
		kwarg=n:length of [bounding box] generated. n=8,tiles=64
		[bounding box]:a discrete square grid, if n increase then expands in +x and -y direction 
		var:htiles = its assured that htiles are only harvestable tiles since we already filtered it
	'''
	global havailable,hslots,EXPBACKOFF
	htiles=MapScanner.get_harvestable_tiles(mid,n=n) 
	if reverse==1 : htiles.reverse()
	if shuffle==1 : htiles=mx.shuffle(htiles)

	LoginManager.save_city()
	fullData=get_all_harvestor_info(CITY)
	LoginManager.load_city()
	hslots=fullData['hslots']
	havailable=	fullData['havailable']
	clearence=MapScanner.gen_tiles(CITY['cid']-(clearence*513),n=clearence*2+1)
	for htile in htiles:
		try:
			TILE=MapScanner.Tile(htile)
		except:
			print('HARVEST:ERROR:Tile Instantiation Failed -',htile)
			return
		if TILE.mid in clearence:
			TILE.data['hcost']+=1
			# print('INFO: CLEARING TILE NIGGA! ',TILE.coords)

		if TILE.coords in fullData['enroutes']:
			print('HARVEST:WARN: redundant mission, Skipping')
			continue

		if havailable==0 :
			print('HARVEST:FAIL: NEED MORE HARVESTERS to ',TILE.coords)
			break

		if hslots==0:
			print('HARVEST:FAIL: R-WORKSHOP MAX MISSIONS LIMIT REACHED')
			break

		state=send_harvestor(CITY,TILE)
		time.sleep(sleep)


def gapchup_city_harvest(CITY):
	custom_harvest(CITY,CITY['sector_root'],n=8,clearence=1)#hemisquareL


if __name__ == '__main__':
	from Defaults import *

	highYieldSector=119080
	while 1:
		try:
			# custom_harvest(CITY1,CITY2['sector_east'],)
			custom_harvest(CITY2,CITY2['sector_east'],clearence=2,shuffle=1,reverse=1)
			custom_harvest(CITY1,CITY2['sector_east'],clearence=2,shuffle=1)
		except Exception as e:
			print('ERROR:',repr(e))

		print("sleeping 120s")
		time.sleep(120)

	"UNIT TESTS"
	# send_harvestor(Defaults.CITY1,MapScanner.Tile(126243))
	# get_all_harvestor_info(CITY1)
	# gapchup_city_harvest(CITY1)

	# print(get_all_harvestor_info(CITY2))