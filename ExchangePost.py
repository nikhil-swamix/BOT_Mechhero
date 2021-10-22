"""
	This module manages the transfer of resources to different cities. 
	we can customize the sending by giving arguments.
"""
from City import *
from __imports__ import *


def make_transfer(FCITY,TCITY,resarray):
	resarray=*map(int,resarray),
	'http://s1.mechhero.com/Building.aspx?sid=35&bt=90'
	apiurl=f'http://s1.mechhero.com/Building.aspx?sid=35&bt=90&cid={FCITY["cid"]}'
	# planet=0 if not TCITY['cid'] <= 385264
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

	print(f"TRANSFER:LOG: F:[{FCITY['name']}]->T:[{TCITY['name']}] resources:{resarray}")
	return LoginManager.post(apiurl,pd)


def transfer_xsurplus(FROMCITY,TOCITY,ignoreincoming=1,
	balance=1,surplusdiv=2,xmin=50000,
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
	receiver=get_res_info(TOCITY)
	sender=get_res_info(FROMCITY)
	surplus=[int(max(0,max(0,a-b)/surplusdiv)) for a,b in zip(sender['current'],xbaseline)]
	sendable=[min(a,b) for a,b in zip(surplus,receiver['deficit'])]
	total_sendable=sum(sendable)
	transporter_max_sendable=get_transporters(FROMCITY)*10000

	if has_incoming_transfers(TOCITY) and not ignoreincoming:
		return print(f'{__name__.upper()}: ALREADY INCOMING TRANSFER @ {TOCITY["name"]}')

	if transporter_max_sendable<=xmin:
		return print(f'TRANSFER:FAIL: Transporters are not available @[{FROMCITY["name"]}]')

	if transporter_max_sendable<=total_sendable:
		scalefactor=transporter_max_sendable/total_sendable
		sendable=[int(n)for n in map(lambda x: x*scalefactor,sendable)]
		print('TRANSFER:WARN: Limiting factors are transporters')

	# print(sendable)

	if sum(sendable)<=xmin:
		return print(f"TRANSFER:FAIL: Min of [{xmin}] required for transferring ")

	if not debug:
		make_transfer(FROMCITY,TOCITY,sendable)
	else:
		print(sender,sendable)
	return True


def topup_new_cities_from_source(source_city,last_n=3,xbaseline=[0,0,10**6]):
	for x in reversed(CITIES[-last_n:]):
		transfer_xsurplus(source_city,x,surplusdiv=1,xbaseline=xbaseline)
		time.sleep(2)

def round_robin_transfer(PRODUCERS=[],CONSUMERS=[],xbaseline=[500000,500000,1000000]):
	# print(f"EXCHANGER:INFO: Starting round Robin Transfer, Sources:{[x['name'] for x in PRODUCERS]}")
	if not CONSUMERS:
		CONSUMERS=[c for c in CITIES if c not in PRODUCERS]
	for p in PRODUCERS:
		c=mx.poprandom(CONSUMERS)
		if not has_incoming_transfers(c):
			transfer_xsurplus(p,c,xbaseline=xbaseline,ignoreincoming=0)
		time.sleep(30)
	print(f"EXCHANGER:INFO: ROUND ROBIN TRANSFER PHINISH! SLEEP 300")


def plan():
	PRODUCERS=[CITY1]
	CONSUMERS=[CITY2]
	while True:
		try:
			round_robin_transfer(PRODUCERS=PRODUCERS,CONSUMERS=CONSUMERS)
		except Exception as e:
			Logger.error(f"{__name__}:{e}")
			LoginManager.login()
		time.sleep(300)
#_________________________________________________
#                 (_)                     | |     
#  _ __ ___   __ _ _ _ __     ___ ___   __| | ___ 
# | '_ ` _ \ / _` | | '_ \   / __/ _ \ / _` |/ _ \
# | | | | | | (_| | | | | | | (_| (_) | (_| |  __/
# |_| |_| |_|\__,_|_|_| |_|  \___\___/ \__,_|\___|
#------------------------------------------------- 

if 	__name__=='__main__':
	# get_transfer_info(CITY15)

	FROM= 	CITY1
	TO=		CITY2

	mechcities=[CITY1]
	xbaseline=[0,0,100000] if FROM in mechcities else [0,0,30000]
	
	transfer_xsurplus(FROM,TO,surplusdiv=1,xbaseline=xbaseline)
	# round_robin_transfer()
	# topup_new_cities_from_source(FROM,last_n=4,xbaseline=xbaseline)
	# plan()