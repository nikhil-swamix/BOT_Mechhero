import requests

DEBUG=0
def get_resources(CITY):
	page=LoginManager.get_page_soup(f"http://s1.mechhero.com/City.aspx?cid={CITY['cid']}")
	ivals=re.search(r'(?<=initialize\().+(?=\))',str(page)).group().split(',')
	crystals=float(ivals[3])
	gas=float(ivals[6])
	cells=float(ivals[9])
	current=(crystals,gas,cells)
	capacity=(float(ivals[4]), float(ivals[7]) ,float(ivals[10]))

	deficit=[round(x,-3) for x in map(lambda x,y: x-y,capacity,current)]
	return {'current':current,'capacity':capacity,'deficit':deficit}

def make_transfer(FCITY,TCITY,resarray):
	resarray=*map(int,resarray),
	'http://s1.mechhero.com/Building.aspx?sid=35&bt=90'
	apiurl=f'http://s1.mechhero.com/Building.aspx?sid=35&bt=90&cid={FCITY["cid"]}'
	pd={
		"__VIEWSTATE": "qxtWJnc7zXieXG7kaEc35je+m512AZkn7dbGma/NUhvUwT2jQJih4NRgX0x6/OPUv4MKUfUuRQhfS7pr7MPI1mifPnMKEHffoyABgXgxQAQ=",
		"rcid": FCITY['cid'],
		"res0": (resarray[0]),
		"res1": (resarray[1]),
		"res2": (resarray[2]),
		"tpid": "0",
		"tx": 	(TCITY['coords'][0]),
		"ty": 	(TCITY['coords'][1]),
		"tid": 	(TCITY['cid']),
		"tcid": (FCITY['cid']),
		"tmv": "-1",
		"tspeed": "20",
		"__VIEWSTATEGENERATOR": "2465F31B",
		"__EVENTTARGET": "ctl00$ctl00$body$content$ctl01",
		"__EVENTARGUMENT": "transfer"
	}

	if DEBUG: print('TRANSFER:DEBUG:',pd)

	print(f"TRANSFER: F:{FCITY['cid']}->T:{TCITY['cid']} resources:{resarray}")
	return LoginManager.post(apiurl,pd)

def transfer_xsurplus(FROMCITY,TOCITY,sdiv=3,xmin=30000,xbaseline=[100000,100000,50000]):
	'''
		will transfer the surplus of SUPPLIER CITY
	'''
	sender=get_resources(FROMCITY)
	receiver=get_resources(TOCITY)
	surplus=[max(0,int(a-b))/2 for a,b in zip(sender['current'],xbaseline)]
	sendable=[min(a,b) for a,b in zip(surplus,receiver['deficit'])]

	if sum(sendable)<=xmin:
		print(f"TRANSFER:FAIL: Min of [{xmin}] required for transferring ")
		return False

	# print(sender,sendable)
	make_transfer(FROMCITY,TOCITY,sendable)
	return True


#________________________________________
#  __  __       ___ __    __  __  __  ___ 
# |  \|__)|\  /|__ |__)  /  `/  \|  \|__  
# |__/|  \| \/ |___|  \  \__,\__/|__/|___ 
#________________________________________
if 	__name__=='__main__':
	from __init__ import *
	PRODUCER=CITY2
	RECIEVER=CITY1

	(transfer_xsurplus(PRODUCER,CITY5))
	# (transfer_xsurplus(PRODUCER,CITY4))
	# (transfer_xsurplus(PRODUCER,CITY3))
	# (transfer_xsurplus(PRODUCER,CITY1))
	# t=make_transfer(PRODUCER,CITY1,resarray)
