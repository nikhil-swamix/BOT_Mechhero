from mxproxy import mx
import requests
import re
import os
import time


#--------------------
proxy=mx.poprandom(mx.jload('database/httpproxies.set.best'))['proxies']
requests=requests.session()
requests.proxies.update(proxy)
print('USING PROXY',requests.proxies)
#--------------------
lastCookie='ASP.NET_SessionId=wn0cwkz5mnhne4wawvlwjr4y; mechhero=3g34hz=&f8wj1h=&4jwhgl=1033&h42sc8=INT&jks2kw=&bi83z1=0'
useragent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
headers={'Cookie':lastCookie, 'User-Agent':useragent }
homepage='http://s1.mechhero.com/City.aspx'
#--------------------

def login():
	posturl='http://s1.mechhero.com/?stage=1'
	postdata={
	"__VIEWSTATE": "ETvKczggEqIm2zf20XFtk0ygFjc0xRMhsE6Qe8Pg4eI1riPD0O9acWDvcWMKOX+teq2k4i/dMP1SMbSXJnr/IWdK9cS17ujwAbUhNAuuHWI=",
	"player": "nikhil7","password": "nikhil999",
	"__VIEWSTATEGENERATOR": "CA0B0334", "__EVENTTARGET": "ctl00$body$ctl00", "__EVENTARGUMENT": "login"
	}
	r1=requests.post(posturl,headers=headers,data=postdata)
	r2=get_page_soup(r1.url).select_one('div a[href*=gamestate]')['href']
	r3=get_page_soup(r2)

def check_login():
	homepagesoup=get_page_soup(homepage)
	if 'container_login' in str(homepagesoup):
		print('boss we are not logged in, auto logging in ...')
		return False	
	else:
		print('logged in') if 'rcid' in str(homepagesoup) else print('login Failed')
		return True

def auto_login():
	if check_login()==False:
		login()
		auto_login() 
	

def get_page_soup(url):
	return mx.get_page_soup(url,headers=headers)

def post(url,data,debug=0):
	req=requests.post(url,headers=headers,data=data,)
	if debug:
		print('posted to',url,'>> redirect_to',req.url)
	return mx.make_soup(req.text)



if __name__ == '__main__':

	# print(get_page_soup(homepage))
	auto_login()
	pass

else:
	auto_login()
	pass
	


	# # print(get_page_soup('http://s1.mechhero.com/City.aspx'))

	# proxy={
	# 	'https':'https://103.236.193.241:84',
	# 	# 'http':mx.get_random_proxy(),
	# 	}

	# result=requests.get(test1,proxies=proxy)
	# print(result)