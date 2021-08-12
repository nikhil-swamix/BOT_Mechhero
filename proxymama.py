from mxproxy import mx
import requests
import os
import time
import random

def funkation(a1,a2):
	time.sleep(random.random()*1)
	print(a1,a2)

def update_proxydb(dbfile,proto,ttl=10,source=1):
	if source==1:
		source1=f'https://api.proxyscrape.com/v2/?request=getproxies&protocol={proto}&timeout=5000&country=all&ssl=all&anonymity=all'
		pset=set(mx.get_page(source1).text.split('\r\n',))
		pset.remove('') if '' in pset else None
	if source==2:
		source2=f'https://www.proxy-list.download/api/v0/get?l=en&t={proto}'
		pset=set()
		for p in mx.get_page(source2).json()[0]['LISTA']:
			pset.add(f'{p["IP"]}:{p["PORT"]}')
		# print(pset)
	mx.setwrite(dbfile,pset)

def proxy_req(url,proxies):
	'''
		tries a post request to proxy and benchmarks the time
	'''
	t=time.time()
	requests.post(url,proxies=proxies,timeout=5,data={'ashil':'bo'})
	tdelta=time.time() - t
	print(f'LOG: {proxies} \t->\tT:{tdelta:.2f}s')
	return {'proxies':proxies,'tat':tdelta}


def proxy_benchmark(dbfile,url,max=1000,proto1='https',proto2='socks4'):
	'''
		arg:dbfile> is a nsv (new line seperated values)
		arg:url> is a standard http/s url to benchmark the proxies
	'''
	mx.maxThreads=256
	data=list(mx.setload(dbfile))[:max]
	print('BENCHMARKING ',len(data),'proxies')
	poolresult=[]
	proxyBenchList=[]
	for x in data:
		proxy={proto1:f'{proto2}://{x}'}
		poolresult.append(mx.apply_async(proxy_req,url,proxy))
	for x in poolresult:
		try: proxyBenchList.append(x.result())
		except :print('badproxy:',x)
	print('sorting')
	proxyBenchList.sort(key=lambda x:x['tat'])
	print('sorting finished!')
	return proxyBenchList

def get_random_proxy():
	randomproxy=mx.poprandom(mx.jload(dbsavefile)[:10])['proxies']
	print(randomproxy)
	r=requests.get('http://teachomatrix.com/',proxies=randomproxy,timeout=5)
	print(r.text)

def refresh_benchmark_proxydb():
	update_proxydb(dbfile,proto2,source=1)
	proxyBenchList=proxy_benchmark(dbfile,ptesturl,proto1=proto1,proto2=proto2)
	mx.jdump(proxyBenchList,dbsavefile)


if __name__ == '__main__':
	DBREFRESHTIMEOUT=1*60
	# ptesturl='https://teachomatrix.com/'
	ptesturl='https://kyliecosmetics.com/'
	dbfile='.\\database\\httpproxies.set';		proto1='http';	proto2='http'
	dbfile='.\\database\\socks5proxies.set';	proto1='http';	proto2='socks5'
	dbfile='.\\database\\socks4proxies.set';	proto1='http';	proto2='socks4'
	dbsavefile=dbfile+'.best'

	# refresh_benchmark_proxydb()



if __name__ == '__main__':
	url='https://ent31lzj50w99.x.pipedream.net'
	url='http://ip-api.com/json/'
	url='https://api.ipify.org?format=json'
	# os.system('schtasks /create /sc onlogon /tn mechherobot /tr _startmain.cmd')

# TEST POOL
# poolresult=[mx.apply_async(funkation,'apple','ball') for x in range(200)]
# [x.result() for x in poolresult]
# print(proxy_benchmark.__doc__,)

