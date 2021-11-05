from __imports__ import *
import LoginManager
import time
from mxproxy import mx

from concurrent.futures import ThreadPoolExecutor
TPOOL=ThreadPoolExecutor(2)
def get_unit_data(UID):
	apiurl=f'http://s1.mechhero.com/data.dt?provider=unit&uid={UID}'
	data=LoginManager.get_page_soup(apiurl)
	# print(apiurl,data)
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
	return [y.result() for y in [TPOOL.submit(get_unit_data,x) for x in get_units_list(CITY)]]

def rearm_repair_all_units(CITY,debug=0,sleep=1):
	# print('INFO: START Rearm+Repair to All units in ',CITY['name'])
	postdata={
		"rcid": CITY['cid'],
		"__VIEWSTATE": "IzwrWd9rYlF+vy4xX1zSXXuu/+4K6em0a7LKgZd70R9WxsLYAjNHSYgekv22BZ2tu5Lmh3FwCmrndZIJ4lWiOIUEJfSUQKyZFXFczbeCOEA=",
		"__VIEWSTATEGENERATOR": "410BFDDA", "__EVENTTARGET": "ctl00$ctl00$body$content$unitControl", "__EVENTARGUMENT": "rearm_7"
	}

	rearm_repair_post={
	"__VIEWSTATE": "/jDwf4ddmwCQokIoy1FTQQZXMyCjJbQSchTxLxzKcPCB+PKKSPoAs1WcIKiUbR5jAj1s7on0u8xATlNuQe23mSMPzvSr9r9KiNms8vUVkR8=",
	"rcid": CITY['cid'],
	"all": "on",
	"group_(null)": "on",
	"groupby": "no+grouping",
	"__VIEWSTATEGENERATOR": "AF2765A0",
	"__EVENTTARGET": "ctl00$ctl00$body$content$ctl00",
	"__EVENTARGUMENT": "rearm"
	}
	ulist=get_units_list(CITY)
	for u in ulist:
		rearm_repair_post[f"unit_{u}"]="on"

	LoginManager.post(f'http://s1.mechhero.com/UnitList.aspx?cid={CITY["cid"]}',rearm_repair_post)
	time.sleep(sleep)
	# uniturls=[f'http://s1.mechhero.com/Unit.aspx?uid={uid}' for uid in ulist]
	# futures=[]
	# for x in uniturls:
	# 	futures.append (POOL.apply_async(LoginManager.post,(x,postdata) ))
	# 	if debug: 
	# 		print(f'LOG: {__name__}:orderedrearm+repair->',x)
	# 	time.sleep(sleep)
	# wait=[r.wait() for r in futures]
	if debug:
		print('INFO: FINISH Rearm+Repair to All units in ',CITY['name'])

def upgrade_unit(uid,CITY):
	posturl=f'http://s1.mechhero.com/Unit.aspx?uid={uid}&tab=upgrade'
	postdata={
	"__VIEWSTATE": "PzBUoPJt06UnlwNlO1aWtzeAhS096m3sTr5Wwk9wTWerSczs5f8o+LehUcvZd5cjVwDvRDIusb5IzsuUHHWxXTLcIWaADzITYrC+6N/j5gw=",
	"rcid": CITY['cid'],
	"rank": "0",
	"__VIEWSTATEGENERATOR": "410BFDDA",
	"__EVENTTARGET": "ctl00$ctl00$body$content$ctl03",
	"__EVENTARGUMENT": "add_1_1"
	}
	unitexpdata=LoginManager.get_page_soup(posturl).select('.progress')
	# print(unitexpdata)

	bonusFields=unitexpdata[-7:]
	bonusCompletion=*map(lambda x:eval(x),[re.search(r"[\d].*",x.text.encode().decode('ascii',errors='ignore')).group() for x in bonusFields]),
	# for x in bonusCompletion: print(x)

	capacity='add_1_1'; repspeed='add_10_1'; crithit='add_14_1'
	print(f"upgrading unit {uid}")

	if bonusCompletion[0]<1:
		postdata['__EVENTARGUMENT']=capacity

	elif bonusCompletion[6]<1:
		postdata['__EVENTARGUMENT']=crithit

	elif bonusCompletion[3]<1:
		postdata['__EVENTARGUMENT']=repspeed

	else:
		return
	# print(postdata['__EVENTARGUMENT'])
	headers={
		"Cookies":"__utma=1.135102907.1628658333.1628658333.1628658333.1; __utmz=1.1628658333.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); mechhero=3g34hz=&f8wj1h=&4jwhgl=1033&h42sc8=INT&jks2kw=&bi83z1=0; ASP.NET_SessionId=grm13ysrxszl2xgnpfq5gtxh",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
		"Referer":"http://s1.mechhero.com/Unit.aspx?uid=86176&tab=upgrade",
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Referer":"http://s1.mechhero.com/Unit.aspx?uid=86176&tab=upgrade", }
	LoginManager.post(posturl,postdata)
	time.sleep(0.3)

def upgrade_all_units(CITY):
	try:
		ulist=get_units_list(CITY)
		*map(upgrade_unit,ulist,[CITY]*len(ulist)),
	except Exception as e:
		print(repr(e))
		LoginManager.login()

if __name__ == '__main__':
	if 'test':
		# upgrade_unit(417119,CITY14)
		upgrade_all_units(CITY1)
		# rearm_repair_all_units(CITY1)
		# get_units_list(CITY1)
		# get_unit_datalist(CITY5)
		...