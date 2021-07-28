import os
import sys
import time

# time.sleep(2)
cityBuilderCommand=os.system('start cmd /K python ./CityBuilder.py ')
time.sleep(2)
autoExploreCommand=os.system('start cmd /K python ./NPCExplorer.py ')
time.sleep(2)
autoHarvestCommand=os.system('start cmd /K python ./Harvester.py ')