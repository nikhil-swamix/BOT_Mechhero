auto_harvest(CITY1,CITY1['sector_root'],shuffle= 1,)
auto_harvest(CITY1,127264,cleartiles=gen_tiles(127265,3))

auto_harvest(CITY2,123176, cleartiles= gen_tiles(125224,3),) 

auto_harvest(CITY3,CITY5['sector_root'],shuffle= 1, cleartiles= gen_tiles(CITY5['sector_root'],3))

auto_harvest(CITY4,119072,)

auto_harvest(CITY5,CITY5['sector_root'])

# auto_harvest(CITY7,CITY7['sector_root'], cleartiles=gen_tiles(121130,3),clearadius=1 )

auto_harvest(CITY8,CITY8['sector_root'], cleartiles=gen_tiles(121130,3),clearadius=1 )


auto_harvest(CITY12,CITY7['sector_root'], cleartiles=gen_tiles(121130,3) )#east
auto_harvest(CITY12,CITY12['sector_root'],)#east

auto_harvest(CITY13,CITY13['sector_root'], cleartiles=gen_tiles(135469,3) )#assist 8

auto_harvest(CITY15,CITY15['sector_root'], cleartiles=gen_tiles(135461,3) )#west

auto_harvest(CITY16,CITY16['sector_root']+8, cleartiles=gen_tiles(142136,3) )#west
auto_harvest(CITY16,CITY16['sector_root']+8+512, cleartiles=gen_tiles(143672,3) )#west
