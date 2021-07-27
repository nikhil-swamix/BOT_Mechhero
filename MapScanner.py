from mxproxy import mx
import LoginManager
import re
import requests
import time


#-------------------------------
class Tile:
	DEBUG=0
	def __init__(self,mid):
		self.mid=mid
		self.rawPage=self.get_raw_page(mid)
		self.pageText=self.get_page_text()
		self.isDebris='debris field' in self.pageText
		self.isEmptyGround='empty ground' in self.pageText
		self.isNPC='NPC location' in self.pageText
		self.coords=self.get_tile_coords(mid)
		self.data=self.analyze_tile()
		
		if Tile.DEBUG==1: 
			[print(k,':',v) for k,v in vars(self).items()]

	def get_tile_coords(self,mid):
		return {"x":(mid%512 -256), "y":(256 -int(mid/512)) }

	def get_raw_page(self,mid):
		return LoginManager.get_page_soup(f'http://s1.mechhero.com/Navigation.aspx?mid={mid}')

	def get_page_text(self):
		return self.rawPage.select_one('.panel.left').text

	def analyze_tile(self,):
		data={}
		if self.isDebris==True:
			data=parse_debris(self.rawPage)
			return data

		if self.isNPC==True:
			data=parse_npc(self.rawPage)
			return data

		if self.isEmptyGround==True:
			pass

#-------------------------------
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
	coords=re.search(r'\(\d.*\d\)',rawPage.select_one('.italic').text).group()
	name=rawPage.select_one('.h2').text
	data={
		'name':name,
		'tiletype':'npc',
		'coords':eval(coords),
		'enemycells':cellUsage,
	}
	# print(data)
	return data


#-------------------------------
def get_root(cid:'mid'):
	xcord=cid%8 
	ycord=(int(cid/512)%8)*512
	cord=(cid-xcord-ycord)
	return (cord)

def gen_tiles(mid,n=8):
	tiles=[x for y in range(mid,mid+512*n,512) for x in range(y,y+n)  ]
	return tiles

def get_map_api_data(mid,n=8):
	apiurl=f'http://s1.mechhero.com/data.map?rq=311_1_{mid}_{n}'
	for x in range(512,(512*n-1)+1,512):
		apiurl+=f'_{mid+x}_{n}'
	page=LoginManager.get_page_soup(apiurl).text
	cleararray=[]
	playerFoundSignal=0
	for x in page.split('%'):
		if re.search(r'5\d',x) and playerFoundSignal==0:
			playerFoundSignal=5
			cleararray.append(x)

		if playerFoundSignal == 4:
			cleararray.append(x)

		if playerFoundSignal == 0:
			cleararray.append(x)

		if  playerFoundSignal> 0:
			playerFoundSignal-=1

	cleararray=cleararray[::2]
	# print(cleararray,len(cleararray))
	return cleararray

def get_harvestable_tiles(mid,n=8):
	tilelist=gen_tiles(mid,n=n)
	datalist=get_map_api_data(mid,n=n)
	hcodes=['20','21','22']
	harvestiles=[x for x,y in zip(tilelist,datalist) if y in hcodes]
	return harvestiles

def get_npc_tiles(mid,n=8):
	tilelist=gen_tiles(mid,n=n)
	datalist=get_map_api_data(mid,n=n)
	ncodes=['30','31','32']
	ntiles=[x for x,y in zip(tilelist,datalist) if y in ncodes]
	return ntiles

if __name__ == '__main__':
	import Defaults
	# CitySector(Defaults.CITY1['cid'])
	mytile=Tile(124704)

	mid=123168
	ntiles=get_npc_tiles(mid)
	print(ntiles)
	# for x in htiles: 
	# 	print(x,Tile(x).isDebris)