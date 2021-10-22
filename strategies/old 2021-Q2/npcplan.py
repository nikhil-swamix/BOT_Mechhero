exploreplans=[
	# [CITY1,CITY1['sector_root']],
	
	[CITY2,123176],
	
	[CITY4,CITY4['sector_root']],#root
	# [CITY4,119080],#east
	# [CITY4,123168],#south

	[CITY5,127280],
	[CITY5,127272],#west
	# [CITY5,123184],#c5north
	
	[CITY7,CITY7['sector_root']],
	
	[CITY8,CITY8['sector_root']],
	# [CITY8,135464],
	# [CITY8,135472],

	# [CITY13,CITY13['sector_root']],
	# [CITY13,CITY13['sector_root']-8],

	# [CITY14,CITY14['sector_root']],
	
	# [CITY15,CITY15['sector_root']],

	[CITY16,CITY16['sector_root']],
	[CITY16,CITY16['sector_root']+8],
	[CITY16,CITY16['sector_root']+4096],
	[CITY16,CITY16['sector_root']+4096+8],
]

for plan in exploreplans:
	auto_explore(*plan)

mechcities=CITIES
for c in mechcities:
	UnitManager.rearm_repair_all_units(c)

