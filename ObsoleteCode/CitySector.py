class CitySector():
	def __init__(self,citymid):
		self.citymid=citymid
		self.rootTile=self.get_root(self.citymid)
		self.tiles=gen_tiles(self.rootTile)

	def get_root(self,cid:'mid'):
		xcord=cid%8 
		ycord=(int(cid/512)%8)*512
		cord=(cid-xcord-ycord)
		return (cord)


def city_sector_harvest(CITY):
	citySector=MapScanner.CitySector(CITY['cid'])
	hslots=get_available_hlsots(CITY)
	for x in citySector.tiles:
		TILE=MapScanner.Tile(x)
		if TILE.isDebris==True:
			resp=send_harvestor(Defaults.CITY1,TILE)
			if resp == 1:
				print('harvestor sent to',TILE.coords)
				hslots-=1

		if hslots==0:
			print('building max simultaneous missions reached')
			break