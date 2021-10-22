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
	serviceRequired=bool(data.select_one('.red') )
	# print('uid:',UID,end='|')
	return {
		'uid':UID,
		'name':name,
		'isFree':isFree,
		'cells':cellUsage,
		'dps':dmgPerSecond,
		'serviceRequired':serviceRequired
		}

def get_units_list(CITY):
	geturl=f'http://s1.mechhero.com/UnitList.aspx?cid={CITY["cid"]}'
	unitlist=[x.attrs['data-uid'] for x in LoginManager.get_page_soup(geturl).select('.ubox')]
	return unitlist

def get_unit_datalist(CITY):
	# global ThreadPool
	return [y.get() for y in [POOL.apply_async(get_unit_data,(x,)) for x in get_units_list(CITY)]]

def rearm_repair_all_units(CITY,debug=0,sleep=1):
	print('INFO: START Rearm+Repair to All units in ',CITY['cid'])
	postdata={
		"rcid": CITY['cid'],
		"__VIEWSTATE": "IzwrWd9rYlF+vy4xX1zSXXuu/+4K6em0a7LKgZd70R9WxsLYAjNHSYgekv22BZ2tu5Lmh3FwCmrndZIJ4lWiOIUEJfSUQKyZFXFczbeCOEA=",
		"__VIEWSTATEGENERATOR": "410BFDDA", "__EVENTTARGET": "ctl00$ctl00$body$content$unitControl", "__EVENTARGUMENT": "rearm_7"
	}
	uniturls=[f'http://s1.mechhero.com/Unit.aspx?uid={uid}' for uid in get_units_list(CITY)]
	futures=[]
	for x in uniturls:
		futures.append (POOL.apply_async(LoginManager.post,(x,postdata) ))
		if debug: 
			print(f'LOG: {__name__}:orderedrearm+repair->',x)
		time.sleep(sleep)

	wait=[r.wait() for r in futures]
	# print('INFO: FINISH Rearm+Repair to All units in ',CITY['cid'])


if __name__ == '__main__':
	'''GET ALL UNITS WITH DATAOBJ'''
	# udatalist=[get_unit_data(x) for x in get_units_list(Defaults.CITY2)]

	'''GET ALL DATA'''
	# udata=get_unit_data(80725)
	# print(udata)

	'''AUTO MAINTAIN ALL UNITS'''
	rearm_repair_all_units(Defaults.CITY1)
