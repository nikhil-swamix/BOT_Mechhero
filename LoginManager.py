from mxproxy import mx
import requests
import re
import os
import time

proxlist=mx.jload('database/socks4proxies.set.best')[:20]

#--------------------
#--------------------
lastCookie='ASP.NET_SessionId=tu2lvt4p3go3rp4hb34dkjsv; mechhero=3g34hz=&f8wj1h=&4jwhgl=1033&h42sc8=INT&jks2kw=&bi83z1=0'
useragent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
headers={'Cookie':lastCookie, 'User-Agent':useragent }
loginpage='http://s1.mechhero.com/Default.aspx'
homepage='http://s1.mechhero.com/City.aspx'
requests=requests.session()

#--------------------
def update_proxy():
	requests.proxies.update(mx.poprandom(proxlist)['proxies'])
	print('PROXY:SET:',requests.proxies)


#--------------------
def get_cookie():
	global lastCookie
	c=requests.get(loginpage)
	lastCookie=';'.join([f'{k}={v}' for k,v in c.cookies.items()])
	print(lastCookie)

def login():
	postdata={
		"__VIEWSTATE": "41/c3qObmn18+xaWQJSXubBkBLKOnESdFi2ZRne2iOPes1OjNXXqJ0yERx9qd3AfzBGsmbylcb1hq0TRQZE+SM+2Qz+qpkQ7pekobz95dXQ=",
		"player": "nikhil7","password": "nikhil999",
		"__VIEWSTATEGENERATOR": "CA0B0334", 
		"__EVENTTARGET": "ctl00$body$ctl00", 
		"__EVENTARGUMENT": "login"
	}
	try:
		# r0=get_page_soup('http://s1.mechhero.com/Default.aspx')
		# postdata.update({'__VIEWSTATE':r0.select_one('#__VIEWSTATE').attrs.get('value')})
		get_cookie()
		r1=requests.post('http://s1.mechhero.com/?stage=1',headers=headers,data=postdata)
		r2=get_page_soup(r1.url).select_one('div a[href*=gamestate]')['href']
		r3=get_page_soup(r2)
		print('LOGIN:INFO: Successfully logged in')
		pass
	except Exception as e:
		print(repr(e))

def check_login(pagestr):
	# if 'container_login' in pagestr:
	if 'rcid' in pagestr:
		print('LOG: Already logged in') 
		return True
	else:
		print('WARN: Boss We Are\'nt Logged In')
		return False
	print('ERROR: login Failed')


def auto_login():
	sniffsoup=mx.get_page_soup(homepage,headers=headers)
	if check_login(str(sniffsoup))==True:
		return
	else:
		update_proxy()
		login()

	auto_login()	
		
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
	response=mx.get_page_soup(url,headers=headers)
	return response

def post(url,data,debug=0):
	try:
		req=requests.post(url,headers=headers,data=data,)
		return mx.make_soup(req.text)
	except :
		print('LOGIN:ERROR: Proxy NOT Responding, load NEW')
		update_proxy()

	if debug:
		print('posted to',url,'>> redirect_to',req.url)


#_________________________________________________
# 					CODE STARTS
#_________________________________________________

if __name__ == '__main__':
	get_cookie()
	pass

else:
	update_proxy()
	auto_login()
	...
	