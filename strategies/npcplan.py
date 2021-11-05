exploreplans = [[CITY1, CITY1['sector_root']], [CITY3, CITY3['sector_root']]]

for plan in exploreplans:
    auto_explore(*plan)

mechcities = CITIES
for c in mechcities:
    UnitManager.rearm_repair_all_units(c)
