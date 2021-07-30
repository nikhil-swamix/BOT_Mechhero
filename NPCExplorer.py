import re
import time
import requests
from mxproxy import mx

#LOGIC MODULES
import Defaults
import LoginManager as lm
from UnitManager import get_unit_datalist,rearm_repair_all_units
from MapScanner import get_npc_tiles,Tile 


#--------------------|
def get_enroutes(CITY):
	militaryTabPage=lm.get_page_soup(f'http://s1.mechhero.com/MissionList.aspx?tab=military&cid={CITY["cid"]}')
	enroutes=militaryTabPage.select('tr.th .green')
	enroutes=[x.parent.parent.find_next_sibling().select_one('td:nth-child(2)').text for x in enroutes]
	enroutes=[eval(re.search(r'\(\d.+\d\)',x).group()) for x in enroutes]
	return enroutes

#--------------------|
def smart_send_units(CITY,TILE,cellRatio=3):
	posturl=f'http://s1.mechhero.com/UnitListSend.aspx?all=1&mid={TILE.mid}&cid={CITY["cid"]}&at=12'
	postdata={
		"__VIEWSTATE": "d7RKjPEUzZ+XmJGCnyQI02PZpb5CNo7VCQnu+D86b0Kpn4zA9Im0+nysgemkIbg6Uzb+lNLgzIoxlzmeY5SzGqE/SoVlQrzm2WUJ0iTBGDY=",
		"rcid": CITY['cid'],
		"tpid": "0",
		"tx": TILE.coords[0], "ty": TILE.coords[1], 
		"tid": '-1', "tcid": CITY['cid'], "tmv": -1,
		"__VIEWSTATEGENERATOR": "B572D792",
		"__EVENTTARGET": "ctl00$ctl00$body$content$unitListSendControl",
		"__EVENTARGUMENT": "wrattack"
	}
	runningCellsSum=0
	enemyCellsMin=TILE.data['enemycells'][0]
	armySendable=False
	udatalist= mx.shuffle([unit for unit in get_unit_datalist(CITY) if unit['isFree']])
	for u in udatalist:
		if u['isFree'] and not u['serviceRequired'] :
			# print (u)
			runningCellsSum+=u['cells']
			postdata.update({f'unit_{u["uid"]}':'on'})
			if runningCellsSum>=cellRatio*enemyCellsMin:
				# print(f'runningCellsSum is {runningCellsSum}, army sendable to {TILE.coords}')
				armySendable=True
				break

	if not armySendable:
		print(f'WARN: STRONGENEMY {TILE.data["name"]} :: OUR POWER ({runningCellsSum}) :: REQ {cellRatio*enemyCellsMin}',)

	if armySendable:
		print('LOG: SENDING ->',TILE.data)
		r=lm.post(posturl,postdata)

#--------------------|
def auto_explore(CITY,sectorId):
	LoginManager.save_city()
	
	enroutes=get_enroutes(CITY)
	ntiles=*map(Tile,get_npc_tiles(sectorId)),
	for TILE in ntiles:
		if TILE.coords in enroutes:
			'skip if mission already undertaken'
			print('Units Already Enroute to',TILE.coords)
			continue
		smart_send_units(CITY,TILE)
	LoginManager.load_city()
	

if __name__ == '__main__':
	import LoginManager
	from Defaults import * 

	EXPBACKOFF=10
	while True:
		try:
			rearm_repair_all_units(CITY2)
			auto_explore(CITY2,CITY2['sector_east'])
		except Exception as e:
			print('ERROR: EXP BCAKOFF TRIGGERED! EXCEEDING API LIMIT!')
			time.sleep((EXPBACKOFF:=EXPBACKOFF*1.2))
			LoginManager.login()
			print(e)

		print("----------\nsleeping 30s\n----------")
		time.sleep(30)

	# get_enroutes(Defaults.CITY1)

	# udatalist= mx.shuffle([unit for unit in UnitManager.get_unit_datalist(Defaults.CITY1) if unit['isFree']])
	# print(Defaults.CITY1['sector_root'])
	# smart_send_units(Defaults.CITY1,MapScanner.Tile(123168),cellRatio=3)




