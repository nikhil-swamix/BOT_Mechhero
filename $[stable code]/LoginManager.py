from mxproxy import mx
import requests
import re
import os
import time

DEBUG=0
#--------------------
browserCookie='ASP.NET_SessionId=v341qipxodjhe2zxeutdn5vj; mechhero=3g34hz=&f8wj1h=&4jwhgl=1033&h42sc8=INT&jks2kw=&bi83z1=0'
lastCookie=''
useragent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
headers={'Cookie':lastCookie, 'User-Agent':useragent}
loginpage='http://s1.mechhero.com/Default.aspx'
homepage='http://s1.mechhero.com/City.aspx'
requestsSession=requests.session()
#--------------------
proxyDBmod=0
def update_proxy():
	global proxyDBmod
	# slot=proxyDBmod%3; proxyDBmod+=1
	proxlist=mx.jload('database/socks4proxies.set.best')[:]
	# proxlist=mx.jload('database/socks5proxies.set.best')[:]
	# proxlist=mx.jload('database/httpproxies.set.best')[:]
	requestsSession.proxies.update(mx.poprandom(proxlist)['proxies'])
	try:
		print('PROXY:NEW:',requestsSession.proxies)
		r=requestsSession.get('http://spicejet.com/',timeout=1)
		print('PROXY: Working')
	except Exception as e:
		print(f"PROXY:FAIL: BAD PROXY",requestsSession.proxies)
		update_proxy()


#--------------------

def login():
	def refresh_cookie():
		global lastCookie
		c=requests.get(loginpage)
		lastCookie=';'.join([f'{k}={v}' for k,v in c.cookies.items()])
		headers.update({'Cookie':lastCookie})
		print("LOGIN:NEWCOOKIE:",lastCookie)
	postdata={
		"__VIEWSTATE": "41/c3qObmn18+xaWQJSXubBkBLKOnESdFi2ZRne2iOPes1OjNXXqJ0yERx9qd3AfzBGsmbylcb1hq0TRQZE+SM+2Qz+qpkQ7pekobz95dXQ=",
		"player": "nikhil7","password": "nikhil999",
		"__VIEWSTATEGENERATOR": "CA0B0334", 
		"__EVENTTARGET": "ctl00$body$ctl00", 
		"__EVENTARGUMENT": "login"
	}
	try:
		# r0=get_page_soup('http://s1.mechhero.com/Default.aspx') # postdata.update({'__VIEWSTATE':r0.select_one('#__VIEWSTATE').attrs.get('value')})

		refresh_cookie()
		r1=requestsSession.post('http://s1.mechhero.com/?stage=1',headers=headers,data=postdata)
		stage2url=get_page_soup(r1.url).select_one('div a[href*=gamestate]')['href']
		r3=get_page_soup(stage2url)
		print('LOGIN:INFO: Successfully logged in')

	except Exception as e:
		update_proxy()
		login()
		# raise e
		print(repr(e))

def check_login():
	sniffsoup=get_page_soup(homepage)

	# if 'container_login' in pagestr:
	if 'rcid' in str(sniffsoup):
		return True
	else:
		return False
	print('ERROR: login Failed')


def auto_login():
	l=check_login()
	if l==True:
		print('LOGIN:INFO: Already logged in') 
		return
	else:
		print('LOGIN:ERROR: Boss We Are\'nt Logged In')
		login()

		
#--------------------
def save_city(debug=0):
	global CITYVAR
	CITYVAR=mx.get_page_soup(homepage,headers=headers).select_one('.current').attrs['href'].split('cid=')[-1]
	if debug:
		print('LOG: city stored')

def load_city(debug=0):
	global CITYVAR
	mx.get_page_soup(f'http://s1.mechhero.com/City.aspx?cid={CITYVAR}',headers=headers)
	if debug:
		print('LOG: city restored')

#--------------------
def get_page_soup(url):
	response=mx.make_soup(requestsSession.get(url,headers=headers).text)
	return response

def post(url,data,debug=0):
	if debug:
		print('LOGIN:POST:DEBUG: posted to',url,data)

	try:

		req=requests.post(url,headers=headers,data=data,)
		return mx.make_soup(req.text)


	except :
		print('LOGIN:POST:ERROR: Proxy/Server is not accepting our post, bloody rascals, load NEW')
		update_proxy()
		return False



#_________________________________________________
# 					CODE STARTS
#_________________________________________________

if __name__ == '__main__':
	# update_proxy()
	# requestsSession.get('https://amir.rachum.com/')
	auto_login()
	# login()


else:
	login()
	# auto_login()

	...
	