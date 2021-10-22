import colorama
colorama.init(autoreset=False)
from colorama import Fore

def success(*msg):
	print(Fore.GREEN,*msg,Fore.RESET,sep='')

def log(*msg):
	print(Fore.WHITE,*msg,Fore.RESET,sep='')

def info(*msg):
	print(Fore.BLUE,*msg,Fore.RESET,sep='')


def warn(*msg):
	print(Fore.YELLOW,*msg,Fore.RESET,sep='')

def error(*msg):
	print(Fore.RED,*msg,Fore.RESET,sep='')


def breakpoint(*msg):

	if msg.__len__()>1:
		msg=" ".join(*msg)
	else:
		msg=msg[0]
	width=50
	offset=int(width/2 - len(msg)/2 +1)
	print("*"*width)
	print(f"{' '*offset}{msg:50}")
	print("*"*width)

if __name__ == '__main__':
	test_text='a dummy hello world messagna'
	for f in [success, log ,info ,warn ,error]:
		f(f.__name__+"\t:"+test_text)
		print('apple ball')

	breakpoint('hekko woarld!')