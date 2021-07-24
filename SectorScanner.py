from mxproxy import mx
import LoginManager
import Defaults
import re
import requests
import time

def gen_tiles(mid,sidelen=8):
	tiles=[x for y in range(mid,mid+512*sidelen,512) for x in range(y,y+sidelen)  ]
	return tiles


class CitySector:
	def __init__(self,citymid):
		self.citymid=citymid
		self.rootTile=self.get_root(self.citymid)
		self.tiles=gen_tiles(self.rootTile)

	def get_root(self,cid:'mid'):
		xcord=cid%8 
		ycord=(int(cid/512)%8)*512
		cord=(cid-xcord-ycord)
		return (cord)


class TileParser:
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
		data={
			'tiletype':'npc',
			'defenderPower':cellUsage,
			'attackMinCells':cellUsage[1]*3

		}
		print(data)
		return data


class Tile:
	DEBUG=0
	def __init__(self,mid):
		# print("Scanning Tile ",mid)
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
		class obj(object):...
		return {
			"x":(mid%512 -256), 
			"y":(256 -int(mid/512))
			}

	def get_raw_page(self,mid):
		return LoginManager.get_page_soup(f'http://s1.mechhero.com/Navigation.aspx?mid={mid}')

	def get_page_text(self):
		return self.rawPage.select_one('.panel.left').text

	def analyze_tile(self,):
		data={}
		if self.isDebris==True:
			data=TileParser.parse_debris(self.rawPage)
			# print(f'tile {self.coords} is a debris',data)
			return data

		if self.isNPC==True:
			data=TileParser.parse_npc(self.rawPage)
			pass

		if self.isEmptyGround==True:
			pass


def get_map_tiles_info(mid,n=8,d=2):
	if d==2:
		arg=''
		...

	apiurl=f'http://s1.mechhero.com/data.map?rq=311_1_{mid}_8'
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
	print(cleararray,len(cleararray))


if __name__ == '__main__':
	# CitySector(Defaults.CITY1['cid'])
	mytile=Tile(126756)
	# get_map_tiles_info(125727)