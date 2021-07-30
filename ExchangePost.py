from Defaults import *

def topup_city_resources(FCITY,TCITY,resdata):
	apiurl='http://s1.mechhero.com/Building.aspx?sid=35&bt=90'
	posturl={
		"__VIEWSTATE": "JpF1fpLXskOuES3D0SSxuXM5N2r4S/Zx1WJwAq2WzxpVI31WqWLuEczesVOfsQencFKiuWR2dD0KGc41TjCRBEJvIluy+QOaNoPrDG1i9Oc=",
		"rcid": FCITY['cid'],
		"res0": resdata['diff'][0],
		"res1": resdata['diff'][1],
		"res2": resdata['diff'][2],
		"tpid": "0",
		"tx": "34",
		"ty": "9",
		"tid": 	TCITY['cid'],
		"tcid": FCITY['cid'],
		"tmv": "-1",
		"tspeed": "20",
		"__VIEWSTATEGENERATOR": "2465F31B",
		"__EVENTTARGET": "ctl00$ctl00$body$content$ctl01",
		"__EVENTARGUMENT": "transfer"
	}

def res_calculator(self):
	pass

if 	__name__=='__main__':
	topup_city_resources()