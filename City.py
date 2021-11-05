'''
	City Module is logical representation of a city, 
	it has info getting functions which will fetch 
	the latest data and status of a city 
'''
from mxproxy import mx
import LoginManager
from MapScanner import *
import Logger

dbfile='database/city.dict'

def get_all_cities_soup():
	slist=LoginManager.get_page_soup('http://s1.mechhero.com/City.aspx').select('#clist a')
	cids=[int(re.search(r'\d+',x['href']).group()) for x in slist]
	return [LoginManager.get_page_soup(f"http://s1.mechhero.com/City.aspx?cid={cid}",sleep=1) for cid in cids]

def refresh_cities_data():
	a=[city_dictifier(x) for x in get_all_cities_soup()]
	mx.jdump(a,dbfile)
	return a 

def load_cities_data(freshcopy=0):
	if mx.fdelta('database/city.dict')>3600*2 or freshcopy:
		print('DEFAULTS:LOG: Fetching fresh copy of all city data')
		refresh_cities_data()
	return mx.jload(dbfile)

def city_dictifier(soup):
	'''take soup make few requests and return crucial city data'''
	cid=int(re.search(r'\d+',soup.select_one('.current')['href']).group())
	blist=get_buildings(soup)
	d={
		'cid':cid,
		'name':soup.select_one('#title').text,
		'coords':get_tile_coords(cid),
		'sector_root':get_root(cid),
		'harvestor_sid':get_sid(blist,'Recycling Workshop'),
		'exchangpost_sid':get_sid(blist,'Exchange Post')
		}
	# print(d)
	return d



def get_sid(blist,btitle,index=0):
	query=[b['sid'] for b in blist if btitle in b['title'] ]
	return  query if query else [-1]

def get_buildings(soup):
	'''
		arg:soup: parse relavant data from soup 
		return: 	a [dict,...] where dict contains crucial info of each building in city
	'''
	buildings=[]
	for x in soup.select('area'):
		title=x.attrs.get('title','')
		sid=int(re.search(r'(?<=sid=)\d*',x['href']).group())
		bt=re.findall(r'(?<=bt=)\d*',x['href'])
		bt=int(bt[0]) if bt else None
		level=int(re.search(r'(?<=\()\d*(?=\))',title).group()) if title else -1
		bdict={'sid':sid,'bt':bt,'title':title,'level':level}
		# print(bdict)
		buildings.append(bdict)
	return buildings

def get_res_info(CITY):
	page=LoginManager.get_page_soup(f"http://s1.mechhero.com/City.aspx?cid={CITY['cid']}")
	ivals=re.search(r'(?<=initialize\().+(?=\))',str(page)).group().split(',')
	crystals=float(ivals[3])
	gas=float(ivals[6])
	cells=float(ivals[9])
	current=(crystals,gas,cells)
	capacity=(float(ivals[4]), float(ivals[7]) ,float(ivals[10]))
	deficit=[round(x,-3) for x in map(lambda x,y: x-y,capacity,current)]
	return {'current':current,'capacity':capacity,'deficit':deficit}

def get_transporters(CITY):
	u= LoginManager.get_page_soup(f'http://s1.mechhero.com/BuildingRouter.aspx?sid=35&bt=90&cid={CITY["cid"]}')
	u=u.select_one('.lpane > p:nth-child(2) > p:nth-child(1) > b:nth-child(2)').text
	transporter_count=int(re.search(r'\d*',u).group())
	# print(transporter_count)
	return transporter_count

def has_incoming_transfers(CITY):
	transferPage=LoginManager.get_page_soup(f'http://s1.mechhero.com/MissionList.aspx?tab=transfer&cid={CITY["cid"]}')
	return bool(transferPage.select('.th .orange'))

def get_all_harvestor_info(CITY):
	'''
		gets basic information about a city's harvesting.
	'''
	citypage= LoginManager.get_page_soup(f'http://s1.mechhero.com/City.aspx?cid={CITY["cid"]}')
	harvestTabPage= LoginManager.get_page_soup(f'http://s1.mechhero.com/MissionList.aspx?tab=harvest&cid={CITY["cid"]}')
	missionDataAJAX= LoginManager.get_page_soup(f'http://s1.mechhero.com/data.dt?provider=misv&cid={CITY["cid"]}&et= 33')

	city_hlevel= int(re.search(r'\d+',citypage.select_one('area[title*="Recycling Workshop"]').attrs['title']).group())
	city_hmissions= harvestTabPage.select('.content .th').__len__()
	hslots= city_hlevel - city_hmissions
	havailable= int(missionDataAJAX.text.split('~')[-1])

	enroutes= harvestTabPage.select('tr.th .green')
	enroutes=[x.parent.parent.find_next_sibling().select_one('td:nth-child(2)').text for x in enroutes]
	enroutes=[eval(re.search(r'\(\d.+\d\)',x).group()) for x in enroutes]

	Logger.info(f'HARVEST:INFO: city={CITY["name"]} hslots=[{hslots}] harvestors={havailable}')
	return {
		'hslots':hslots,
		'havailable':havailable,
		'enroutes':enroutes
		}

def get_military_enroutes(CITY):
	militaryTabPage=LoginManager.get_page_soup(f'http://s1.mechhero.com/MissionList.aspx?tab=military&cid={CITY["cid"]}')
	enroutes=militaryTabPage.select('tr.th .green')
	enroutes=[x.parent.parent.find_next_sibling().select_one('td:nth-child(2)').text for x in enroutes]
	enroutes=[eval(re.search(r'\(\d.+\d\)',x).group()) for x in enroutes]
	return enroutes

if __name__ == '__main__':
	LoginManager.login()
	# print(city_dictifier(LoginManager.get_page_soup('http://s1.mechhero.com/City.aspx?cid=142646')))

	if "test":
		load_cities_data(freshcopy=1)
		# get_all_cities_soup(); 

	# mx.fwrite('./apple.data','anshul')
	# mx.jdump(refresh_cities_data(),'apple.data')