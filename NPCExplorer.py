import re
import time
from mxproxy import mx
from MapScanner import get_npc_tiles,Tile 

from __imports__ import *
#LOGIC MODULES

#--------------------|
def get_enroutes(CITY):
	militaryTabPage=LoginManager.get_page_soup(f'http://s1.mechhero.com/MissionList.aspx?tab=military&cid={CITY["cid"]}')
	enroutes=militaryTabPage.select('tr.th .green')
	enroutes=[x.parent.parent.find_next_sibling().select_one('td:nth-child(2)').text for x in enroutes]
	enroutes=[eval(re.search(r'\(\d.+\d\)',x).group()) for x in enroutes]
	return enroutes

#--------------------|
from UnitManager import get_unit_datalist,rearm_repair_all_units
def smart_send(CITY,TILE,cellRatio=3.5):
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
		print(f'NPC:WARN: Strongenemy {TILE.data["name"]} :: OUR POWER ({runningCellsSum}) :: REQ {cellRatio*enemyCellsMin}',)

	if armySendable:
		print('NPC:SEND: DEST->',TILE.data)
		r=LoginManager.post(posturl,postdata)

#--------------------|
def auto_explore(CITY,sectorId,sleep=1):
	print('NPC:INFO: START Scanning city=',CITY['cid'],'in sector=',sectorId)
	enroutes=get_enroutes(CITY)
	ntiles=*map(Tile,get_npc_tiles(sectorId)),
	for TILE in ntiles:
		if TILE.coords in enroutes:
			print('NPC:WARN: Units Already Enroute, skipping',TILE.coords)
			continue
		smart_send(CITY,TILE)
		time.sleep(sleep)
	

def plan1(sleep=1):
		#CITY2
		auto_explore(CITY2,CITY2['sector_east'],sleep=sleep)
		UnitManager.rearm_repair_all_units(CITY2,sleep=sleep)
		#CITY3
		auto_explore(CITY3,127272,sleep=sleep)# mini explore tiles
		UnitManager.rearm_repair_all_units(CITY3,sleep=sleep)
		print('NPC:INFO: scanner cooldown 60s')



if __name__ == '__main__':
	from __imports__ import *
	progbackoff=30
	progfactor=2
	while True:
		try:
			plan1()
		except Exception as e:
			progbackoff+=progfactor
			LoginManager.auto_login()
			print(f'NPC:ERROR: {e}')
		time.sleep(progbackoff)

	'''TESTING'''
	...
	
