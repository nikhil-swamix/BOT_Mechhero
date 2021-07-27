from mxproxy import mx
import LoginManager
import Defaults
import re
import requests
import time
from pprint import pprint
lastCookie=LoginManager.lastCookie

def get_buildings(cityID):
	cityurl=f'http://s1.mechhero.com/City.aspx?cid={cityID}'
	page=LoginManager.get_page_soup(cityurl)
	buildings=[]
	for x in page.select('area'):
		title=x.attrs.get('title','')
		sid=int(re.search(r'(?<=sid=)\d*',x['href']).group())
		bt=re.findall(r'(?<=bt=)\d*',x['href'])
		bt=int(bt[0]) if bt else None
		level=int(re.search(r'(?<=\()\d*(?=\))',title).group()) if title else -1
		d={'sid':sid,'bt':bt,'title':title,'level':level}
		buildings.append(d)
	return buildings

def build_order(cityID,sid,bt):
	postpayload={
	"__VIEWSTATE": "oyzb4H5sU2dLgDogNyBqS3zmA5AUeA1sze5fHIr5Oz5a5zTUBsSBtQ6Hf4jsPaeWuiEHUCWkRlo3RKm10YEV/fd/gf/syomjwyeFz3aRQz4=",
	"rcid": cityID,
	"__VIEWSTATEGENERATOR": "2465F31B",
	"__EVENTTARGET": f"ctl00$ctl00$body$content$building{bt}",
	"__EVENTARGUMENT": "build"
	}
	headers={'Cookie':LoginManager.lastCookie}
	response=requests.post(f'http://s1.mechhero.com/Building.aspx?sid={sid}&bt={bt}',headers=headers, data=postpayload)
	print(f"build order placed :: cityID={cityID},sid={sid},bt={bt} ")


def autobuild(cityID,bt=0,strategy='lowest',maxlvl=20,randmode=1):
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

		# [print(x) for x in buildTargets]
		for t in buildTargets:
			build_order(cityID,t['sid'],t['bt'])
			...
		# for building in minBuilding:

	# build_order(Defaults.CITY1,32,1)

if __name__ == '__main__':

	while True:
		# autobuild(Defaults.CITY1['cid'],bt=[11],maxlvl=10)
		autobuild(Defaults.CITY2['cid'],bt=[3],maxlvl=10)

		# print(LoginManager.get_page_soup('http://s1.mechhero.com/City.aspx'))
		print("sleeping 60s")
		time.sleep(60)
		# autobuild(Defaults.CITY1,bt=[11,12,13],maxlvl=6)




