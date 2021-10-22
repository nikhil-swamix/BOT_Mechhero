"""
	This module automates the process of exploring NPCs in the game. 
	flagship function "auto_explore" which allows uninterrupted and smart execution of NPC tiles.
"""

import re
import time
from mxproxy import mx
from MapScanner import get_npc_tiles,Tile 
from __imports__ import *
from City import *
import UnitManager
# import multiprocessing as mp

# import colorama
# colorama.init()

#--------------------|
from UnitManager import get_unit_datalist,rearm_repair_all_units
def smart_send(CITY,TILE,cellRatio=3,debug=0):
	posturl=f'http://s1.mechhero.com/UnitListSend.aspx?all=1&mid={TILE.mid}&cid={CITY["cid"]}&at=12'
	postdata={
		"__VIEWSTATE": "d7RKjPEUzZ+XmJGCnyQI02PZpb5CNo7VCQnu+D86b0Kpn4zA9Im0+nysgemkIbg6Uzb+lNLgzIoxlzmeY5SzGqE/SoVlQrzm2WUJ0iTBGDY=",
		"rcid": CITY['cid'], "tpid": "0",
		"tx": TILE.coords[0], "ty": TILE.coords[1], 
		"tid": '-1', "tcid": CITY['cid'], "tmv": -1,
		"__VIEWSTATEGENERATOR": "B572D792", "__EVENTTARGET": "ctl00$ctl00$body$content$unitListSendControl", "__EVENTARGUMENT": "wrattack"
	}
	armySendable=False
	runningCellsSum=0
	enemyCellsMin=TILE.data['enemycells'][0]
	armySendCells=int(enemyCellsMin*(cellRatio+(enemyCellsMin/3000)))
	udatalist= mx.shuffle([unit for unit in get_unit_datalist(CITY) if unit['isFree']])
	for u in udatalist:
		if u['isFree'] and not u['serviceRequired'] :
			# print (u)
			runningCellsSum+=u['cells']
			postdata.update({f'unit_{u["uid"]}':'on'})
			if runningCellsSum>=armySendCells:
				# print(f'runningCellsSum is {runningCellsSum}, army sendable to {TILE.coords}')
				armySendable=True
				break

	if armySendable:
		Logger.success('NPC:SEND: DEST->','|'.join([f'{k}={v}' for k,v in TILE.data.items()]))
		r=LoginManager.post(posturl,postdata)

	if not armySendable and debug:
		Logger.warn(f'NPC: Strongenemy {TILE.data["name"]} :: OUR POWER ({runningCellsSum}) :: REQ {armySendCells}',)

#--------------------|
def auto_explore(CITY,sectorId,sleep=1):
	'''
		desc: automatically explore a given sector from particular city by sending mechs.
		apple
		args:CITY: City Object imported from defaults.py
	'''
	Logger.info('NPC: START Scanning city=',CITY['name'],' in sector=',sectorId)
	enroutes=get_military_enroutes(CITY)
	ntiles=*map(Tile,get_npc_tiles(sectorId)),
	for TILE in ntiles:
		if TILE.coords in enroutes:
			Logger.warn('NPC: Units Already Enroute, skipping',TILE.coords)
			continue
		smart_send(CITY,TILE)
		time.sleep(sleep)

#--------------------|
def plan():
	""" 
	implements the plan in the live text file. 
	if the contents of the dependency "strategies/npcplan.py" 
	change then the strategy also changes in realtime since exec is used.
	"""
	while True:
		try:
			exec(mx.fread('strategies/npcplan.py'))
		except Exception as e:
			print(__name__,e)
			LoginManager.login()
		time.sleep(10)


if __name__ == '__main__':
	# auto_explore(CITY8,131376)#noob sector
	# auto_explore(CITY5,CITY5['sector_root'])
	# print(math.exp(5))
	# smart_send(CITY1,Tile(118536))
	plan()
	...
