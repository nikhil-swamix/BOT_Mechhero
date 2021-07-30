from mxproxy import mx
import re
import time

import Defaults
import LoginManager
import ExchangePost

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

		sid=int(re.search(r'(?<=sid=)\d*',x['href']).group())
		bt=re.findall(r'(?<=bt=)\d*',x['href'])
		bt=int(bt[0]) if bt else None
		level=int(re.search(r'(?<=\()\d*(?=\))',title).group()) if title else -1
		bdict={'sid':sid,'bt':bt,'title':title,'level':level}
		# print(bdict)
		buildings.append(bdict)
	return buildings

#------------------------------
def build(cityID,sid,bt):
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

def autobuild(cityID,btype=0,maxlvl=20,onlyidle=0,randmode=1):
	'''
		desc:
			select lowest building from each type and then place build order on them
		example:
			for example input 'bt' is a list [1,2,3] then crystal,gas,cells are polulated 
			and lowest building is placed order , total of 3 orders are placed in this case
		arg:cityID: 
			standard id argument of city
		arg:btype:
			building type which player wants to build, see the game's main docs for more info.
		kwarg:randmode:
			randomize build order? and remove any priorities,
		kwarg:maxlvl:
			max level the building can be placed order, target buildings higher than this level are ignored 
	'''
	LoginManager.save_city()
	buildTargets=[]
	buildings=get_buildings(cityID)

	if randmode:
		btype=mx.shuffle(btype)

	if type(btype) is not list: 
		btype=list(btype)

	if onlyidle: 
		b=[]
		for x in buildings:
			if 'building now' in x['title'] or 'queued' in x['title']:
				print('skipping',x)
				continue
			else:
				b.append(x)
		buildings=b

	# print(buildings)
	for b in btype:
		try:
			filteredList=list(filter(lambda x:x['bt']==b, buildings))
			# print('fl',filteredList)
			minBuilding=sorted(filteredList, key=lambda x:x['level'])[0]
			if minBuilding['level']>=maxlvl:
				print(f'skipping {minBuilding} , reason=maxlevel reached')
				continue
			else: 
				buildTargets.append(minBuilding)

		except Exception as e:
			pass

	# print('btargets',buildTargets)
	[build(cityID,t['sid'],t['bt']) for t in buildTargets]
	return LoginManager.load_city()

#_________________________________________________
from Defaults import *

def city1plan():
	'matured'

def city2plan():
	autobuild(CITY2['cid'],btype=[45],maxlvl=20)

def city3plan():
	autobuild(CITY3['cid'],btype=[15,41,30,32,42],maxlvl=10)
	# autobuild(CITY3['cid'],btype=[*range(100)],maxlvl=10)
	# autobuild(CITY3['cid'],btype=[3],maxlvl=10)
#_________________________________________________

                                                                                         
if __name__ == '__main__':
	# city2plan()
	city3plan()
	# print(get_resources(Defaults.CITY3))

