from mxproxy import mx
import requests
import re
import os
import time

requests=requests.session()
print(dir(requests))
print((requests.proxies))
lastCookie='ASP.NET_SessionId=wn0cwkz5mnhne4wawvlwjr4y; mechhero=3g34hz=&f8wj1h=&4jwhgl=1033&h42sc8=INT&jks2kw=&bi83z1=0'
useragent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
headers={'Cookie':lastCookie,'User-Agent':useragent}
	

def login():
	posturl='http://s1.mechhero.com/?stage=1'
	postdata={
	"__VIEWSTATE": "033+KqTo8WLb2e67Y+sgT4c6Z9FdyXMHklG0HkVNh+K2J23FU6d6xIYm2kVNInXwPGB1qXTd0LRE8KGnZQahd6FQdoURCsEAauRpB/CFF5U=",
	"player": "nikhil7",
	"password": "nikhil999",
	"__VIEWSTATEGENERATOR": "CA0B0334",
	"__EVENTTARGET": "ctl00$body$ctl00",
	"__EVENTARGUMENT": "login"
	}
	d=requests.post(posturl,headers=headers,data=postdata)
	
def get_page_soup(url):
	return mx.get_page_soup(url,headers=headers)

def post(url,data):
	# print('posting to',url)
	return mx.make_soup(requests.post(url,headers=headers,data=data).text)

def burst_request(fn,datatuple):
	futurelist=[TransmitPool.submit(get_page_soup,testurl) for x in datatuple]
	...

if __name__ == '__main__':
	'http://s1.mechhero.com/?stage=1'
	# login()
	testurl='https://docs.python.org/'
	# print(get_page_soup('http://s1.mechhero.com/City.aspx'))

	proxy=mx.get_random_proxy()
	print(proxy)