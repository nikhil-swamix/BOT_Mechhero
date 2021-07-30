from mxproxy import mx
import re
import requests
import time
from pprint import pprint

def get_resources(CITY):
	page=LoginManager.get_page_soup(f"http://s1.mechhero.com/City.aspx?cid={CITY['cid']}")
	ivals=re.search(r'(?<=initialize\().+(?=\))',str(page)).group().split(',')
	crystals=float(ivals[3])
	crystalsMax=float(ivals[4])
	gas=float(ivals[6])
	gasMax=float(ivals[7])
	cells=float(ivals[9])
	cellsMax=float(ivals[10])

	current=(crystals,gas,cells)
	max=(crystalsMax, gasMax ,cellsMax)
	diff=[round(x,-3) for x in map(lambda x,y: x-y,max,current)]
	return {'current':current,'max':max,'diff':diff}

#------------------------------
def get_buildings(cityID):
	'''
		arg:cityID> city id which the player wants get its building list. 
		return> 	a [dict,...] where dict contains crucial info of each building in city
	'''
	cityurl=f'http://s1.mechhero.com/City.aspx?cid={cityID}'
	page=LoginManager.get_page_soup(cityurl)
	buildings=[]
	for x in page.select('area'):
		title=x.attrs.get('title','')
		if 'building now' in title or 'queued' in title:
			print(f'LOG: @{cityID} skipping {title}')
			continue
		sid=int(re.search(r'(?<=sid=)\d*',x['href']).group())
		bt=re.findall(r'(?<=bt=)\d*',x['href'])
		bt=int(bt[0]) if bt else None
		level=int(re.search(r'(?<=\()\d*(?=\))',title).group()) if title else -1
		buildings.append({'sid':sid,'bt':bt,'title':title,'level':level})
	return buildings

#------------------------------
def build_order(cityID,sid,bt):
	"""
		arg:cityID> city id which the player wants get its building list. 
		arg:sid>	specific id of tile which needs to be upgraded.
		arg:bt>		type of building present on the sid
		var:postpayload> this object was seperately captured via browser requests
		return> None, since its a post function. and its output is junk
	"""
	postpayload={
	"__VIEWSTATE": "oyzb4H5sU2dLgDogNyBqS3zmA5AUeA1sze5fHIr5Oz5a5zTUBsSBtQ6Hf4jsPaeWuiEHUCWkRlo3RKm10YEV/fd/gf/syomjwyeFz3aRQz4=",
	"rcid": cityID,
	"__VIEWSTATEGENERATOR": "2465F31B",
	"__EVENTTARGET": f"ctl00$ctl00$body$content$building{bt}",
	"__EVENTARGUMENT": "build"
	}

	response=LoginManager.post(f'http://s1.mechhero.com/Building.aspx?sid={sid}&bt={bt}',postpayload)
	print(f"build order placed :: cityID={cityID},sid={sid},bt={bt} ")


#------------------------------
def autobuild(cityID,bt=0,strategy='lowest',maxlvl=20,randmode=1):
	'''
		arg:cityID> 
	'''
	LoginManager.save_city()
	buildTargets=[]
	if randmode:
		bt=mx.shuffle(bt)

	if strategy=='lowest':
		if type(bt) is int:
			bt=[bt]
		for btype in bt:
			filteredList=filter(lambda x:x['bt']==btype, get_buildings(cityID))
			minBuilding=sorted(filteredList, key=lambda x:x['level'])[0]
			if minBuilding['level']>=maxlvl:
				print(f'skipping {minBuilding} , reason=maxlevel reached')
				continue
			else:
				buildTargets.append(minBuilding)
		for t in buildTargets:
			build_order(cityID,t['sid'],t['bt'])

	return LoginManager.load_city()


#_________________________________________________
#                  _                       _      
#                 (_)                     | |     
#  _ __ ___   __ _ _ _ __     ___ ___   __| | ___ 
# | '_ ` _ \ / _` | | '_ \   / __/ _ \ / _` |/ _ \
# | | | | | | (_| | | | | | | (_| (_) | (_| |  __/
# |_| |_| |_|\__,_|_|_| |_|  \___\___/ \__,_|\___|
#_________________________________________________

                                                                                         
if __name__ == '__main__':
	import Defaults
	import LoginManager
	import ExchangePost
	CRONSLEEP=60
	while True:
		# autobuild(Defaults.CITY1,bt=[11,12,13],maxlvl=6)
		autobuild(Defaults.CITY3['cid'],bt=[3],maxlvl=10)
		print(f'SLEEP: sleeping for {CRONSLEEP}s');time.sleep(CRONSLEEP);CRONSLEEP+=1




	print(get_resources(Defaults.CITY3))

