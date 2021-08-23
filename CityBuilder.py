"""
	City builder module automates the development of buildings in the city

"""
from mxproxy import mx
import re
import time
import LoginManager
from Defaults import *



#-------------------------------------------------
# 	___ 					   _	
#  / __)                  _   (_)                              
# | |__ _   _ ____   ____| |_  _  ___  ____   ___              
# |  __) | | |  _ \ / ___)  _)| |/ _ \|  _ \ /___)             
# | |  | |_| | | | ( (___| |__| | |_| | | | |___ |             
# |_|   \____|_| |_|\____)\___)_|\___/|_| |_(___/                                                               
#-------------------------------------------------

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
def build(CITY,sid,bt,debug=0):
	"""
		arg:CITY: 	city id which the player wants get its building list. 
		arg:sid:	specific id of tile which needs to be upgraded.
		arg:bt:		type of building present on the sid
		var:postpayload> this object was seperately captured via browser requests,ti imitate build order
		return> None, since its a post function. and its output is junk
	"""
	postpayload={
	"__VIEWSTATE": "oyzb4H5sU2dLgDogNyBqS3zmA5AUeA1sze5fHIr5Oz5a5zTUBsSBtQ6Hf4jsPaeWuiEHUCWkRlo3RKm10YEV/fd/gf/syomjwyeFz3aRQz4=",
	"rcid": CITY['cid'],
	"__VIEWSTATEGENERATOR": "2465F31B",
	"__EVENTTARGET": f"ctl00$ctl00$body$content$building{bt}",
	"__EVENTARGUMENT": "build"
	}

	response=LoginManager.post(f'http://s1.mechhero.com/Building.aspx?sid={sid}&bt={bt}',postpayload,debug=debug)
	if response:
		print(f"BUILDER:INFO: order placed in city[{CITY['name']}],sid={sid},bt={bt} ")
	else:
		print(f'BUILDER:ERROR: failed post response: bool=False ')

	time.sleep(1)


#------------------------------
def autobuild(CITY,btype,maxlvl=20,onlyidle=1,randmode=1,batchsize=2):
	'''
		desc:
			select lowest building from each type and then place build order on them
		example:
			for example input 'bt' is a list [1,2,3] then crystal,gas,cells are polulated 
			and lowest building is placed order , total of 3 orders are placed in this case
		arg:CITY: 
			standard id argument of city, its a dict
		arg:btype:
			building type which player wants to build, see the game's main docs for more info. 
			a new copy is created.
		kwarg:randmode:
			randomize build order? and remove any priorities,
		kwarg:maxlvl:
			max level the building can be placed order, target buildings higher than this level are ignored 
	'''

	buildTargets=[]
	allBuildings=get_buildings(CITY['cid'])

	if type(btype) is not list: #type conversion
		btype=[btype] #print("BUILDER: Please provide btype argument as list ~ [1,2,3]...")

	if randmode:
		btype=mx.shuffle(btype[:])

	if onlyidle: 
		b=[]
		for x in allBuildings:
			if 'building now' in x['title'] or 'queued' in x['title']:
				print('skipping',x)
				continue
			else:
				b.append(x)
		allBuildings=b


	# print('trace >>>>>>>>>>>>>>>>',btype)
	for b in btype:
		try:
			filteredList=list(filter(lambda x:x['bt']==b, allBuildings))
			if filteredList:
				minBuilding=sorted(filteredList, key=lambda x:x['level'])[0]
				if minBuilding['level']>=maxlvl:
					print(f'BUILDER:LOG: skipping {minBuilding} , reason=maxlevel reached')
					continue
				buildTargets.append(minBuilding)

		except Exception as e:
			print(e)

	# print('btargets',buildTargets)
	[build(CITY,t['sid'],t['bt']) for t in buildTargets[0:batchsize]]
	return 

#_________________________________________________CONSTANTS
class Buildings:
	core= [29, 30, 32, 41, 42]
	mines={'crystal':1,'gas':2,'cells':3}
	storages=[11,12,13,15]
	defense=[45,46,17]

#_________________________________________________
def develop_new_cities(lastn=4):
	for CITY in CITYLIST:
		autobuild(CITY,storages,maxlvl=18)#build these to lvl-1 first
		time.sleep(2)


def plan():
	# autobuild(CITY7,[3,0],maxlvl=18)#build these to lvl-1 first
	newcities=list(reversed(CITIES[-4:]))
	new_city_base_plan=[3,0]+Buildings.core
	for c in newcities:
		autobuild(c,  new_city_base_plan,maxlvl=18)#build these to lvl-1 first
		autobuild(c,  Buildings.storages,maxlvl=10)#build these to lvl-1 first

	# time.sleep(60)



#_________________________________________________
#                 (_)                     | |     
#  _ __ ___   __ _ _ _ __     ___ ___   __| | ___ 
# | '_ ` _ \ / _` | | '_ \   / __/ _ \ / _` |/ _ \
# | | | | | | (_| | | | | | | (_| (_) | (_| |  __/
# |_| |_| |_|\__,_|_|_| |_|  \___\___/ \__,_|\___|
#-------------------------------------------------                                                              
if __name__ == '__main__':
	# print(__file__)
	plan()
	# while True:
	# 	autobuild(CITY6,[3,3,3],maxlvl=10)
	# 	time.sleep(60)

