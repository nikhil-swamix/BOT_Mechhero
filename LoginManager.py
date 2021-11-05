from mxproxy import mx
import requests
import re
import os 
import time 
import pickle
import random
# import multiprocessing as mp

#----------------------------------------
DEBUG=0
headers={'Cookie':'', 'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"}
homepage='http://s1.mechhero.com/City.aspx'
requestsSession=requests.session()
cookieboxPath='database/cookiebox.json'
cookiebox=mx.jload(cookieboxPath)
cookieIndexFileCounter='database/cookiebox.index'
proxyDBmod=0
#----------------------------------------
def update_proxy():
	global proxyDBmod
	# slot=proxyDBmod%3; 
	# proxyDBmod+=1
	# proxlist=mx.jload('database/socks5proxies.set.best')[:]
	# proxlist=mx.jload('database/httpproxies.set.best')[:]
	try:
		proxlist=mx.jload('database/socks4proxies.set.best')[:20]
		requestsSession.proxies.update(mx.poprandom(proxlist)['proxies'])
		r=requestsSession.get('http://spicejet.com/',timeout=3)
		print('PROXY:NEW:',requestsSession.proxies,'and is Working')
	except Exception as e:
		print(f"PROXY:FAIL: UNABLE TO REACH PROXY",requestsSession.proxies)

#----------------------------------------
def get_cookie():
	c=requests.get('http://s1.mechhero.com/Default.aspx')
	cookie=mx.make_cookie(c)
	return cookie

def get_cookies(count=5):
	cookies=[get_cookie() for x in range(count)]
	cookiebox=mx.jdump(cookies,cookieboxPath)

def iter_cookiebox():
	cookieIterIndex=int(mx.fread(cookieIndexFileCounter))
	mx.fincrement(cookieIndexFileCounter)
	# print('cookie iter index:',cookieIterIndex)
	return cookiebox[cookieIterIndex%len(cookiebox)]

def login_cookiebox():
	for x in mx.jload(cookieboxPath):
		login(cookie=x)

def login(cookie=''):
	mx.touch(cookieIndexFileCounter,data='0')
	postdata={
		"__VIEWSTATE": "41/c3qObmn18+xaWQJSXubBkBLKOnESdFi2ZRne2iOPes1OjNXXqJ0yERx9qd3AfzBGsmbylcb1hq0TRQZE+SM+2Qz+qpkQ7pekobz95dXQ=",
		"player": "censored","password": "censored", #{"player": "yourname", "password": "yourpass"} load from credentials.json file
		"__VIEWSTATEGENERATOR": "CA0B0334", 
		"__EVENTTARGET": "ctl00$body$ctl00", 
		"__EVENTARGUMENT": "login"
	}
	postdata.update(mx.jload('./database/credentials.json')) #load and update_password
	# print(mp.current_process()._identity)
	if cookie:
		headers['Cookie']=cookie
	else:
		headers['Cookie']=iter_cookiebox()
		time.sleep(random.random())
	try:
		if not is_logged_in():
			# r0=get_page_soup('http://s1.mechhero.com/Default.aspx') # postdata.update({'__VIEWSTATE':r0.select_one('#__VIEWSTATE').attrs.get('value')})
			r1=requestsSession.post('http://s1.mechhero.com/?stage=1',headers=headers,data=postdata)
			r2=get_page_soup(r1.url).select_one('div a[href*=gamestate]')['href']
			r3=get_page_soup(r2)
			print('LOGIN:INFO: new logged in with cookie',headers['Cookie'][:30])
		else:
			print('LOGIN:INFO: already logged in with',headers['Cookie'][:30])

	except Exception as e:
		print(repr(e))
		# update_proxy()
		time.sleep(5)
		login()


#----------------------------------------
def is_logged_in():
	sniffsoup=get_page_soup(homepage)
	# if 'container_login' in pagestr:
	if 'rcid' in str(sniffsoup):
		return True
	else:
		return False
	print('ERROR: login Failed')


def auto_login():
	if is_logged_in():
		print('LOGIN:INFO: Already logged in') 
		return
	else:
		print('LOGIN:ERROR: Boss We Are\'nt Logged In')
		login()

#--------------------
def get_page_soup(url,debug=0,sleep=0.1):
	# headers['Cookie']=iter_cookiebox()
	response=mx.make_soup(requestsSession.get(url,headers=headers).text)
	if debug:
		print('LOGINMANAGER:DEBUG:',url)
	time.sleep(sleep)
	return response

def post(url,data,headers=headers,debug=0,sleep=0.1):
	if debug:
		print('LOGIN:POST:DEBUG: posted to',url,headers,data)

	try:
		req=requestsSession.post(url,headers=headers,data=data,)
		time.sleep(sleep)
		return mx.make_soup(req.text)

	except Exception as e:
		print('LOGIN:POST:ERROR: Proxy/Server is not accepting our post, bloody rascals, load NEW')
		login()
		return False

#______________________________________________________________________________

if __name__ == '__main__':
	# get_cookies(5)
	login_cookiebox()
	# [print(iter_cookiebox()) for x in range(15) ]
	...
