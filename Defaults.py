import LoginManager
from MapScanner import get_tile_coords,get_root
import re
from mxproxy import mx
# from  CityBuilder import get_buildings

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

def city_dict(soup):
	'''take soup make few requests and return crucial city data'''
	cid=int(re.search(r'\d+',soup['href']).group())
	blist=get_buildings(cid)
	# print(cid)
	return {
		'cid':cid,
		'name':soup.contents[0],
		'coords':get_tile_coords(cid),
		'sector_root':get_root(cid),
		'harvestor_sid':get_sid(blist,'Recycling Workshop'),
		'exchangpost_sid':get_sid(blist,'Exchange Post')
		}


dbfile='database/city.dict'
def save_cities_data():
	masterpage=LoginManager.get_page_soup('http://s1.mechhero.com/City.aspx')
	cities=masterpage.select('#clist a')
	mx.jdump([city_dict(x) for x in cities],dbfile) 


def load_cities_data(freshcopy=0):
	if freshcopy:
		print('DEFAULTS:LOG: Fetching fresh copy of all city data')
		save_cities_data()
	return mx.jload(dbfile)


def get_sid(blist,btitle,index=0):
	query=[b['sid'] for b in blist if btitle in b['title'] ]
	return  query if query else [-1]

#_________________________________________________/
CITIES=load_cities_data()
for i,cd in enumerate(CITIES):
	exec(f'CITY{i+1}=cd')



# print(cities)