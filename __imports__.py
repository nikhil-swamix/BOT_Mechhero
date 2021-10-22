'''this is doc'''
import time,os,re,random

import City
import colorama
import LoginManager
import Logger
colorama.init(autoreset=False)



#_________________________________________________
LoginManager.login()
CITIES=City.load_cities_data(freshcopy=0)
for i,cd in enumerate(CITIES):
	exec(f'CITY{i+1}=cd')
