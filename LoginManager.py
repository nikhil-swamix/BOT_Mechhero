from mxproxy import mx
import requests
import re
import os
import time

proxlist=mx.jload('database/socks4proxies.set.best')[:20]

#--------------------
#--------------------
lastCookie='ASP.NET_SessionId=wn0cwkz5mnhne4wawvlwjr4y; mechhero=3g34hz=&f8wj1h=&4jwhgl=1033&h42sc8=INT&jks2kw=&bi83z1=0'
useragent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
headers={'Cookie':lastCookie, 'User-Agent':useragent }
homepage='http://s1.mechhero.com/City.aspx'
loginstate=0

#--------------------
def update_proxy():
	requests.proxies.update(mx.poprandom(proxlist)['proxies'])
	print('PROXY:',requests.proxies)


#--------------------
def login():
	postdata={
		"__VIEWSTATE": "41/c3qObmn18+xaWQJSXubBkBLKOnESdFi2ZRne2iOPes1OjNXXqJ0yERx9qd3AfzBGsmbylcb1hq0TRQZE+SM+2Qz+qpkQ7pekobz95dXQ=",
		"player": "nikhil7","password": "nikhil999",
		"__VIEWSTATEGENERATOR": "CA0B0334", 
		"__EVENTTARGET": "ctl00$body$ctl00", 
		"__EVENTARGUMENT": "login"
	}
	# r0=get_page_soup('http://s1.mechhero.com/Default.aspx')
	# postdata.update({'__VIEWSTATE':r0.select_one('#__VIEWSTATE').attrs.get('value')})
	r1=requests.post('http://s1.mechhero.com/?stage=1',headers=headers,data=postdata)
	r2=get_page_soup(r1.url).select_one('div a[href*=gamestate]')['href']
	r3=get_page_soup(r2)
	print('login sukkess')

#--------------------
def save_city():
	global CITYVAR
	CITYVAR=mx.get_page_soup(homepage,headers=headers).select_one('.current').attrs['href'].split('cid=')[-1]


#--------------------
def load_city():
	global CITYVAR
	mx.get_page_soup(f'http://s1.mechhero.com/City.aspx?cid={CITYVAR}',headers=headers)
	print('city restored')


#--------------------
def check_login(pagestr):
	global loginstate
	if 'container_login' in pagestr:
		loginstate=0
		print('WARN: Boss We Are\'nt Logged In')
		return False
	if 'rcid' in pagestr:
		loginstate=1
		print('LOG: Already logged in') 
		return True
	print('ERROR: login Failed')


def auto_login():
	sniffsoup=mx.get_page_soup(homepage,headers=headers)
	if not check_login(str(sniffsoup)):
		login()

#--------------------

def get_page_soup(url):
	response=mx.get_page_soup(url,headers=headers)
	return response

#--------------------
def post(url,data,debug=0):
	try:
		req=requests.post(url,headers=headers,data=data,)
		return mx.make_soup(req.text)
	except :
		print('update proxy')
		update_proxy()

	if debug:
		print('posted to',url,'>> redirect_to',req.url)



if 'module call':
	requests=requests.session()
	update_proxy()


if __name__ == '__main__':
	auto_login()
	pass

	


	# # print(get_page_soup('http://s1.mechhero.com/City.aspx'))

	# proxy={
	# 	'https':'https://103.236.193.241:84',
	# 	# 'http':mx.get_random_proxy(),
	# 	}

	# result=requests.get(test1,proxies=proxy)
	# print(result)