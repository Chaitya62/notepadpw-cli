#!/usr/bin/env python3
'''

Usage: npwcli FILE LINK


Examples:

	npwcli test.py testingthiscli


Options:
-h, --help

'''

from docopt import docopt
from npwcli.update_content import Notepad
from termcolor import cprint
import os




def start():
	arguments = docopt(__doc__)
	#print(arguments)
	filename = arguments.get('FILE', None)
	curr_dir = os.getcwd()
	file_path = os.path.join(curr_dir, filename)


	link = arguments.get('LINK', None)


	try: 

		cprint('Conneting to notepad.pw....','green')

		notepad = Notepad(link)

	except Exception as e:

		cprint("\nError: Something went wrong...", 'red')
		return -1

	if(notepad.haspw):
		cprint('\nPASS: The given url is password protected', 'yellow')
	else:
		cprint("\nSaving {} to {}..... \n".format(filename,link), 'green')
		notepad.save_file(file_path, True)



	



