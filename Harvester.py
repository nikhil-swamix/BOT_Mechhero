from mxproxy import mx
import re
import requests
import time

import Defaults
import LoginManager
import SectorScanner

def available_hlsots(CITY):
	citypage=LoginManager.get_page_soup(f'http://s1.mechhero.com/City.aspx?cid={CITY["cid"]}')
	city_hlevel=int(re.search(r'\d',citypage.select_one('area[title*="Recycling Workshop"]').attrs['title']).group())

	citypage=LoginManager.get_page_soup(f'http://s1.mechhero.com/MissionList.aspx?tab=harvest&cid={CITY["cid"]}')
	city_hmissions=citypage.select('.content .th').__len__()

	empty_slots=city_hlevel - city_hmissions
	print(empty_slots)
	return empty_slots

	
def send_harvestor(CITY:'object',TILE):
	'''
	ARGSDEF:
		CITY: class object from SectorScanner
		TILE: class object from SectorScanner
	'''
	if TILE.data['hcost']==0:
		print("debris below threshold",TILE.coords)
		return 0

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
	resp=LoginManager.post(apiurl,postdata)
	# print(resp)
	return 1
	# print(d.text) 

def auto_harvest(CITY):
	citySector=SectorScanner.CitySector(CITY['cid'])
	hslots=available_hlsots(CITY)
	for x in citySector.tiles:
		TILE=SectorScanner.Tile(x)
		if TILE.isDebris==True:
			resp=send_harvestor(Defaults.CITY1,TILE)
			if resp == 1:
				print('harvestor sent to',TILE.coords)
				hslots-=1

		if hslots==0:
			print('building max simultaneous missions reached')
			break

		time.sleep(0.5)

if __name__ == '__main__':
	auto_harvest(Defaults.CITY1)
	# available_hlsots(Defaults.CITY1)
	# send_harvestor(Defaults.CITY1,SectorScanner.Tile(126243))