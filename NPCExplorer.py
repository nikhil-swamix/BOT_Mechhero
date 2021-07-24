import re
import time
import requests
from mxproxy import mx

#LOGIC MODULES
import Defaults
import LoginManager
import SectorScanner



def send_units(CITY,TILE):
	postdata={
		"__VIEWSTATE": "d7RKjPEUzZ+XmJGCnyQI02PZpb5CNo7VCQnu+D86b0Kpn4zA9Im0+nysgemkIbg6Uzb+lNLgzIoxlzmeY5SzGqE/SoVlQrzm2WUJ0iTBGDY=",
		"rcid": "126754",
		"all": "on",
		"group_(null)": "on",
		"unit_80474": "on",
		"unit_80725": "on",
		"unit_81063": "on",
		"unit_81532": "on",
		"unit_86176": "on",
		"unit_48345": "on",
		"tpid": "0",
		"tx": "36",
		"ty": "9",
		"tid": "-1",
		"tcid": "126754",
		"tmv": "20",
		"__VIEWSTATEGENERATOR": "B572D792",
		"__EVENTTARGET": "ctl00$ctl00$body$content$unitListSendControl",
		"__EVENTARGUMENT": "wrattack"
	}
	posturl=f'http://s1.mechhero.com/UnitListSend.aspx?at=12&mid=126756&all=0&uid=48345%2c32129%2c251%2c338%2c469%2c4644&h=1700436'

def auto_explore(CITY):
	...