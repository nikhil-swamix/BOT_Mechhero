"""
	This module manages the transfer of resources to different cities. 
	we can customize the sending by giving arguments.
"""
from __imports__ import *
DEBUG=0

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
	u=u.select_one('.lpane > p:nth-child(3) > b:nth-child(2)').text
	transporter_count=int(re.search(r'\d*',u).group())
	return transporter_count

def make_transfer(FCITY,TCITY,resarray):
	resarray=*map(int,resarray),
	'http://s1.mechhero.com/Building.aspx?sid=35&bt=90'
	apiurl=f'http://s1.mechhero.com/Building.aspx?sid=35&bt=90&cid={FCITY["cid"]}'
	pd={
		"__VIEWSTATE": "qxtWJnc7zXieXG7kaEc35je+m512AZkn7dbGma/NUhvUwT2jQJih4NRgX0x6/OPUv4MKUfUuRQhfS7pr7MPI1mifPnMKEHffoyABgXgxQAQ=",
		"rcid": FCITY['cid'], "tid": 	(TCITY['cid']), "tcid": (FCITY['cid']),
		"res0": (resarray[0]), "res1": (resarray[1]), "res2": (resarray[2]),
		"tpid": "0",
		"tx": 	(TCITY['coords'][0]), "ty": 	(TCITY['coords'][1]),
		"tmv": "-1",
		"tspeed": "20",
		"__VIEWSTATEGENERATOR": "2465F31B", "__EVENTTARGET": "ctl00$ctl00$body$content$ctl01", "__EVENTARGUMENT": "transfer"
	}

	if DEBUG: print('TRANSFER:DEBUG:',pd)

	print(f"TRANSFER:LOG: F:[{FCITY['name']}]->T:[{TCITY['name']}] resources:{resarray}")
	return LoginManager.post(apiurl,pd)


def transfer_xsurplus(FROMCITY,TOCITY,
	balance=1,surplusdiv=2,xmin=30000,
	xbaseline=[100000,100000,100000],
	debug=0):
	'''
		desc:
			smart function to balance resources between Producer and consumer cities,
			will transfer the surplus production of SUPPLIER CITY to destination CITY,

		note:
			1.get_res_info, of "to" and "from" citie.
			2.calculate surplus with offset to xbaseline. 
			3.take min function of (deficit and surplus) to avoid overflow.
			3.check transporters and multiplyX10000 to get max sendable.
	'''
	print(f"TRANSFER:INFO: Initiating transfer [{FROMCITY['name']}]->[{TOCITY['name']}]")
	sender=get_res_info(FROMCITY)
	receiver=get_res_info(TOCITY)
	surplus=[int(max(0,max(0,a-b)/surplusdiv)) for a,b in zip(sender['current'],xbaseline)]
	sendable=[min(a,b) for a,b in zip(surplus,receiver['deficit'])]
	total_sendable=sum(sendable)
	transporter_max_sendable=get_transporters(FROMCITY)*10000

	if transporter_max_sendable<=xmin:
		return print(f'TRANSFER:FAIL: Transporters are not available @[{FROMCITY["name"]}]')

	if transporter_max_sendable<=total_sendable:
		scalefactor=transporter_max_sendable/total_sendable
		sendable=[int(n)for n in map(lambda x: x*scalefactor,sendable)]
		print('TRANSFER:WARN: Limiting factors are transporters')

	# print(sendable)

	if sum(sendable)<=xmin:
		print(f"TRANSFER:FAIL: Min of [{xmin}] required for transferring ")
		return False

	if not debug:
		make_transfer(FROMCITY,TOCITY,sendable)
	else:
		print(sender,sendable)
	return True


def topup_new_cities_from_source(source_city,last_n=3,xbaseline=[]):
	for x in reversed(CITIES[-last_n:]):
		transfer_xsurplus(source_city,x,surplusdiv=1,xbaseline=xbaseline)
		time.sleep(2)

#_________________________________________________
#                 (_)                     | |     
#  _ __ ___   __ _ _ _ __     ___ ___   __| | ___ 
# | '_ ` _ \ / _` | | '_ \   / __/ _ \ / _` |/ _ \
# | | | | | | (_| | | | | | | (_| (_) | (_| |  __/
# |_| |_| |_|\__,_|_|_| |_|  \___\___/ \__,_|\___|
#------------------------------------------------- 
if 	__name__=='__main__':


	FROM= 	CITY7
	TO=		CITY11
	xbaseline=[00000,00000,700000]

	transfer_xsurplus(FROM,TO,surplusdiv=1,xbaseline=xbaseline)
	# topup_new_cities_from_source(FROM,last_n=4,xbaseline=xbaseline)