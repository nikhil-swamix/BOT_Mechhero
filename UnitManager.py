import Defaults
import LoginManager
import time

from multiprocessing.pool import ThreadPool
POOL=ThreadPool(8)
# from threading import Thread

def get_unit_data(UID):
	apiurl=f'http://s1.mechhero.com/data.dt?provider=unit&uid={UID}'
	data=LoginManager.get_page_soup(apiurl)
	name=data.select_one('.name').text
	status=data.select_one('.status').text
	isFree=True if 'Standing-by' in status else False
	dmgPerSecond=sum(int(x.text) for x in data.select('.damage b'))
	cellUsage=int(data.select_one('.res').text)
	# print('uid:',UID,end='|')
	return {'uid':UID,'name':name,'isFree':True,'dps':dmgPerSecond,'cells':cellUsage}

def get_units_list(CITY):
	geturl=f'http://s1.mechhero.com/UnitList.aspx?cid={CITY["cid"]}'
	unitlist=[x.attrs['data-uid'] for x in LoginManager.get_page_soup(geturl).select('.ubox')]
	return unitlist

def get_unit_datalist(CITY):
	# global ThreadPool
	return [y.get() for y in [POOL.apply_async(get_unit_data,(x,)) for x in get_units_list(CITY)]]

def rearm_repair_all_units(CITY):
	postdata={
		"__VIEWSTATE": "IzwrWd9rYlF+vy4xX1zSXXuu/+4K6em0a7LKgZd70R9WxsLYAjNHSYgekv22BZ2tu5Lmh3FwCmrndZIJ4lWiOIUEJfSUQKyZFXFczbeCOEA=",
		"rcid": CITY['cid'],
		"__VIEWSTATEGENERATOR": "410BFDDA",
		"__EVENTTARGET": "ctl00$ctl00$body$content$unitControl",
		"__EVENTARGUMENT": "rearm_7"
	}

	futures=[]
	# futures.append( (t:=Thread(target=LoginManager.post,args=[uniturl,postdata])) );t.start();
	# futures.append( threadchunk)

	uniturls=[f'http://s1.mechhero.com/Unit.aspx?uid={uid}' for uid in get_units_list(CITY)]
	for x in uniturls:
		futures.append (POOL.apply_async(LoginManager.post,(x,postdata) ))
		print('LOG: orderedrearm+repair->',x)
		time.sleep(0.5)

	try: [r.wait() for r in futures]
	except: [r.join() for r in futures]

if __name__ == '__main__':
	'''GET ALL UNITS'''
	# ulist=get_units_list(Defaults.CITY1)

	'''GET ALL DATA'''
	# udata=get_unit_data(ulist[1])

	'''AUTO MAINTAIN ALL UNITS'''
	rearm_repair_all_units(Defaults.CITY1)
