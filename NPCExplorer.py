"""
	This module automates the process of exploring NPCs in the game. 
	flagship function "auto_explore" which allows uninterrupted and smart execution of NPC tiles.
"""

import re
import time
from mxproxy import mx
from MapScanner import get_npc_tiles,Tile 

from __imports__ import *

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
		print('NPC:SEND: DEST->','|'.join([f'{k}={v}' for k,v in TILE.data.items()]))
		r=LoginManager.post(posturl,postdata)

#--------------------|
def auto_explore(CITY,sectorId,sleep=1):
	'''
		desc: automatically explore a given sector from particular city by sending mechs.
		apple
		args:CITY: City Object imported from defaults.py
	'''
	print('NPC:INFO: START Scanning city=',CITY['name'],'in sector=',sectorId)
	enroutes=get_enroutes(CITY)
	ntiles=*map(Tile,get_npc_tiles(sectorId)),
	for TILE in ntiles:
		if TILE.coords in enroutes:
			print('NPC:WARN: Units Already Enroute, skipping',TILE.coords)
			continue
		smart_send(CITY,TILE)
		time.sleep(sleep)

#--------------------|
def plan():
	""" 
	implements the plan in the live text file. 
	if the contents of the dependency "npcplan.py" change then the strategy also changes in realtime 
	"""
	try:
		exec(mx.fread('strategies/npcplan.py'))
	except:
		LoginManager.login()

def plancron():	
	"""continuous plan exec in while loop"""
	while True:
		print('----------| NPC SEQUENCE START 	   |----------')
		try:
			plan()
		except Exception as e:
			print(f'MAIN:NPC:ERROR {repr(e)}')
			LoginManager.login()
			errsignal=1
		time.sleep(10)


if __name__ == '__main__':
	from __imports__ import *
	# auto_explore(CITY8,131376)#noob sector
	auto_explore(*[CITY7,135472])
	# plan()

if 'a'=='b':pass