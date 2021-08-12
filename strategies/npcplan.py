exploreplans=[
	[CITY2,123176],
	
	[CITY4,CITY4['sector_root']],#root
	[CITY4,119080],#east
	[CITY4,123168],#south

	[CITY5,127280],
	[CITY5,127272],
	[CITY5,123184],
	
	[CITY7,CITY7['sector_root']],
	
	[CITY8,131376],
	[CITY8,135464],
	[CITY8,135472],
]

for ep in exploreplans:
	auto_explore(*ep)
	...

mechcities=[CITY2, CITY4, CITY5, CITY7, CITY8,]
for c in mechcities:
	UnitManager.rearm_repair_all_units(c)

