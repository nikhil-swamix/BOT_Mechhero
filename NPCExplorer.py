import re
import time
import requests
from mxproxy import mx

#LOGIC MODULES
import Defaults
import LoginManager
import MapScanner
import UnitManager


def smart_send_units(CITY,TILE,cellRatio=3):
	global udatalist
	# preposturl=f'http://s1.mechhero.com/Navigation.aspx?mid={TILE.mid}'
	# prepostdata={
	# 	"__VIEWSTATE": "GijoGdyZyvGwMydP0WTvSZAJHJ47f3KMsQ0EZx6oMGPuQJrNn8Q5NxA4ua8wHe7Ms9IqKla9Wl3gqKrNOllF491y3c0bW+V6yalYpn1mKUs=",
	# 	"rcid": CITY['cid'],
	# 	"__VIEWSTATEGENERATOR": "366D9E7C",
	# 	"__EVENTTARGET": "ctl00$ctl00$body$content$navigationControl",
	# 	"__EVENTARGUMENT": "send"
	# }
	# print(LoginManager.post(preposturl,prepostdata))


	posturl=f'http://s1.mechhero.com/UnitListSend.aspx?all=1&mid={TILE.mid}&cid={CITY["cid"]}&at=12&uid=48345,32129,251,338,469,4644'
	postdata={
		"__VIEWSTATE": "d7RKjPEUzZ+XmJGCnyQI02PZpb5CNo7VCQnu+D86b0Kpn4zA9Im0+nysgemkIbg6Uzb+lNLgzIoxlzmeY5SzGqE/SoVlQrzm2WUJ0iTBGDY=",
		"rcid": CITY['cid'],
		"tpid": "0",
		"tx": TILE.coords["x"],
		"ty": TILE.coords["y"],
		"tid": '-1',
		"tcid": "126754",
		"tmv": -1,
		"__VIEWSTATEGENERATOR": "B572D792",
		"__EVENTTARGET": "ctl00$ctl00$body$content$unitListSendControl",
		"__EVENTARGUMENT": "wrattack"
	}
	runningCellsSum=0
	enemyCellsMin=TILE.data['enemycells'][0]
	armySendable=False
	for u in udatalist:
		if u['isFree']:
			runningCellsSum+=u['cells']
			postdata.update({f'unit_{u["uid"]}':'on'})
			if runningCellsSum>=cellRatio*enemyCellsMin:
				print(f'runningCellsSum is {runningCellsSum}, army sendable to {TILE.data}')
				armySendable=True
				break

	if not armySendable:
		print(f'WARN: LOW ARMY CELLS ({runningCellsSum})->',TILE.data)

	if armySendable:
		print('LOG: SENDING ->',TILE.data)
		r=LoginManager.post(posturl,postdata)



def auto_explore(CITY,sectorId):
	global udatalist
	for x in MapScanner.get_npc_tiles(sectorId):
		udatalist= mx.shuffle([unit for unit in UnitManager.get_unit_datalist(CITY) if unit['isFree']])
		smart_send_units(CITY,MapScanner.Tile(x))
	

if __name__ == '__main__':
	while True:
		UnitManager.rearm_repair_all_units(Defaults.CITY1)
		auto_explore(Defaults.CITY1,Defaults.CITY1['sector_root'])
		print("\n______\nsleeping 60s\n______\n"),time.sleep(60)


	# udatalist= mx.shuffle([unit for unit in UnitManager.get_unit_datalist(Defaults.CITY1) if unit['isFree']])
	# smart_send_units(Defaults.CITY1,MapScanner.Tile(123168),cellRatio=3)
	# print(Defaults.CITY1['sector_root'])




	# mid=Defaults.CITY1['sector_root']
	# print(mid)
	# bp=8
	# for x in MapScanner.get_map_api_data(mid):
	# 	print(x,end='\t|')
	# 	bp+=1
	# 	if bp % 8 ==0: print()