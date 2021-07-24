import Defaults
import LoginManager
import time
def get_all_units(CITY):
	geturl=f'http://s1.mechhero.com/UnitList.aspx?cid={CITY["cid"]}'
	unitlist=[x.attrs['data-uid'] for x in LoginManager.get_page_soup(geturl).select('.ubox')]
	print(unitlist)
	return unitlist


from multiprocessing.pool import ThreadPool
POOL=ThreadPool(8)
from threading import Thread
def rearm_repair_all_units(CITY):

	postdata={
	"__VIEWSTATE": "IzwrWd9rYlF+vy4xX1zSXXuu/+4K6em0a7LKgZd70R9WxsLYAjNHSYgekv22BZ2tu5Lmh3FwCmrndZIJ4lWiOIUEJfSUQKyZFXFczbeCOEA=",
	"rcid": CITY['cid'],
	"__VIEWSTATEGENERATOR": "410BFDDA",
	"__EVENTTARGET": "ctl00$ctl00$body$content$unitControl",
	"__EVENTARGUMENT": "rearm_7"
	}

	futures=[]
	for uid in get_all_units(CITY):
		uniturl=f'http://s1.mechhero.com/Unit.aspx?uid={uid}'
		# futures.append( (t:=Thread(target=LoginManager.post,args=[uniturl,postdata])) );t.start();

		threadchunk=POOL.apply_async(LoginManager.post,[uniturl,postdata])
		futures.append( threadchunk)
		# LoginManager.post(uniturl,postdata)
		time.sleep(0.01)


	try:
		[r.wait() for r in futures]
	except:
		[r.join() for r in futures]



if __name__ == '__main__':
	# get_all_units(Defaults.CITY1)
	rearm_repair_all_units(Defaults.CITY1)

