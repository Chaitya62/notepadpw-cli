#!/usr/bin/python3

'''

Usage: cli.py FILE LINK


Examples:

	python3 cli.py test.py


Options:
-h, --help

'''

from docopt import docopt
from spider import Spider
from termcolor import cprint
import os




def start():
	arguments = docopt(__doc__)
	#print(arguments)
	filename = arguments.get('FILE', None)
	curr_dir = os.getcwd()
	file_path = os.path.join(curr_dir, filename)


	link = arguments.get('LINK', None)
	link = "https://notepad.pw/" + link


	try: 

		cprint('Conneting to notepad.pw....','green')

		spy = Spider(link)

	except Exception as e:

		cprint("\nError: Something went wrong...", 'red')
		return -1

	if(spy.url_key == '' and spy.pad_key == ''):
		cprint('\nPASS: The given url is password protected', 'yellow')
	else:
		cprint("\nSaving {} to {}..... \n".format(filename,link), 'green')
		spy.save(file_path, True)



	



	# if(filename):
	# 	print(filename)


start()
