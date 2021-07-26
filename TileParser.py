import re 
def parse_debris(rawPage):
	resources=[int(x.text) for x in rawPage.select('.scroll_y > span:nth-child(1) span')]
	data={
		'tiletype':'debris',
		'resources':resources,
		'total':(total:=sum(resources)),
		'hcost':int(total/2000)
		}
	return data

def parse_npc(rawPage):
	cellUsage=*map(int,re.findall(r'\d+',rawPage.select_one('div.panel:nth-child(1) > p:nth-child(4)').text)),
	coords=re.match(r'\(\)',rawPage.select_one('.italic'))
	data={
		'tiletype':'npc',
		'defenderPower':cellUsage,
		'coord':eval(coords)
	}
	# print(data)
	return data

if __name__ == '__main__':
	...