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
		self.pagesoup=self.get_raw_page(mid)
		self.pagetext=self.get_page_text()
		self.isDebris='debris field' in self.pagetext
		self.isEmptyGround='empty ground' in self.pagetext
		self.isNPC='NPC location' in self.pagetext
		self.coords=get_tile_coords(mid)
		self.data=self.analyze_tile()
		if Tile.DEBUG==1: 
			[print(k,':',v) for k,v in vars(self).items()]


	def get_raw_page(self,mid):
		return LoginManager.get_page_soup(f'http://s1.mechhero.com/Navigation.aspx?mid={mid}')

	def get_page_text(self):
		return self.pagesoup.select_one('.panel.left').text

	def analyze_tile(self,):
		data={}
		if self.isDebris==True: return parse_debris(self.pagesoup)
		if self.isNPC==True: return parse_npc(self.pagesoup)
		if self.isEmptyGround==True: pass

#------------------------------->GETTERS
def get_tile_coords(mid):
	x=(mid%512 -256)
	y=(256 -int(mid/512))
	return (x,y)
#------------------------------->TILE ROOT FINDER
def get_root(mid):
	xcord=mid%8 
	ycord=(int(mid/512)%8)*512
	cord=(mid-xcord-ycord)
	return (cord)

#------------------------------->TILE GENERATOR
def gen_tiles(mid,n=8):
	tiles=[x for y in range(mid,mid+512*n,512) for x in range(y,y+n)  ]
	return tiles

#------------------------------->PARSERS
def parse_debris(pagesoup):
	resources=[int(x.text) for x in pagesoup.select('.scroll_y > span:nth-child(1) span')]

	data={
		'tiletype':'debris',
		'resources':resources,
		'has_equipment':pagesoup.select_one('.tiny_eq').__bool__() ,
		'total':(total:=sum(resources)),
		'hcost':int(total/2000)
		}
	return data

def parse_npc(pagesoup):
	cellUsage=*map(int,re.findall(r'\d+',pagesoup.select_one('div.panel:nth-child(1) > p:nth-child(4)').text)),
	coords=re.search(r'\(\d.*\d\)',pagesoup.select_one('.italic').text).group()
	name=pagesoup.select_one('.h2').text
	data={
		'name':name,
		'tiletype':'npc',
		'coords':eval(coords),
		'enemycells':cellUsage,
	}
	# print(data)
	return data



#-------------------------------
def prettyprint_map_api_tiles(mid,n=8):
	# mid=Defaults.CITY1['sector_root']
	print(mid)
	bp=8
	for x in get_map_api_data(mid):
		print(x,end='\t|')
		bp+=1
		if bp % 8 ==0: print()

def get_map_api_data(mid,n=8):
	apiurl=f'http://s1.mechhero.com/data.map?rq=83_1_{mid}_{n}'
	for x in range(512,(512*n-1)+1,512):
		apiurl+=f'_{mid+x}_{n}'
	page=LoginManager.get_page_soup(apiurl).text
	# print("trace",page)
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
	datalist=get_map_api_data(mid,n=n)
	hcodes=['20','21','22']
	harvestiles=[x for x,y in zip(gen_tiles(mid,n=n),datalist) if y in hcodes]
	return harvestiles

def get_npc_tiles(mid,n=8):
	datalist=get_map_api_data(mid,n=n)
	ncodes=['30','31','32']
	ntiles=[x for x,y in zip(gen_tiles(mid,n=n),datalist) if y in ncodes]
	return ntiles

if __name__ == '__main__':
	print (get_root(117002))
	LoginManager.login()
	# CitySector(Defaults.CITY1['cid'])
	# mid=123168
	ntiles=get_npc_tiles(114952)
	print(ntiles)
