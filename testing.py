from mxproxy import mx
import requests
import os
import time
import random

def funkation(a1,a2):
	time.sleep(random.random()*1)
	print(a1,a2)


if __name__ == '__main__':
	url='https://ent31lzj50w99.x.pipedream.net'
	url='http://ip-api.com/json/'
	url='https://api.ipify.org?format=json'
	# proxy=get_proxy_api()
	proxy={'http':'http://167.71.5.83:3128',}#neder
	proxy={'https':'https://194.233.69.90:443'}#singapoor
	proxy={'https':'https://79.143.87.138:9090'}#UK https

	proxy={'http':'http://185.204.187.22:6000'}#japan https


	# print(data)
	# from fp.fp import FreeProxy
	# # proxy={'http':FreeProxy().get()}
	# proxy={'https':f'https://{data.pop()}'}
	# print(proxy)

	# r=requests.get(url,proxies=proxy)
	# print(r.text)

def proxy_req(url,proxies):
	t=time.time()
	requests.get(url,proxies=proxies,timeout=3,params={'dp':'sotta'})
	tdelta=time.time() - t
	print(f'via {proxies} -> took {tdelta:.2f}s')
	return {'proxies':proxies,'tat':tdelta}

def proxy_benchmark(dbfile,url,proto1='https',proto2='socks4'):
	'''
		arg:dbfile> is a nsv (new line seperated values)
		arg:url> is a standard http/s url to benchmark the proxies
	'''
	mx.maxThreads=256
	data=list(mx.setload(dbfile))[:]
	print('BENCHMARKING ',len(data),'proxies')
	poolresult=[]
	proxyBenchList=[]
	for x in data:
		proxy={proto1:f'{proto2}://{x}'}
		poolresult.append(mx.apply_async(proxy_req,url,proxy))
	for x in poolresult:
		try: proxyBenchList.append(x.result())
		except :pass
	print('sorting')
	proxyBenchList.sort(key=lambda x:x['tat'])
	print('sorting finished!')
	return proxyBenchList


dbfile='.\\database\\httpproxies.set';		proto1='https';	proto2='https'
dbfile='.\\database\\socks5proxies.set';	proto1='http';	proto2='socks5'
dbfile='.\\database\\socks4proxies.set';	proto1='http';	proto2='socks4'

result=proxy_benchmark(dbfile,'https://www.spicejet.com/',proto1=proto1,proto2=proto2)
mx.jdump(result,dbfile+'.best')

# TEST POOL
# poolresult=[mx.apply_async(funkation,'apple','ball') for x in range(200)]
# [x.result() for x in poolresult]


# print(proxy_benchmark.__doc__,)

