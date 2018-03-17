#!/usr/bin/env python3
"""
Notepad.pw CLI

Usage: 	
	npw [options] FILE LINK


Example:
	npw -lo test.py testingthiscli

Options:
-h, --help      	Show this screen
--version       	Show version
-l, --live-update   Enable live update on notepad
-o, --overwrite     Overwrite notepad contents

"""

import os

from docopt import docopt
from termcolor import cprint
from pprint import pprint


from npwcli.update_content import Notepad
from npwcli import __version__





def start():


	arguments = docopt(__doc__, version='npw version '+'.'.join(str(i) for i in __version__))
	

	filename = arguments.get('FILE', None)
	curr_dir = os.getcwd()
	file_path = os.path.join(curr_dir, filename)


	live_update = arguments.get('--live-update', False)



	link = arguments.get('LINK', None)


	try: 

		cprint('Connecting to notepad.pw....','blue')

		notepad = Notepad(link, live_update=live_update)

	except Exception as e:

		cprint("\nError: Something went wrong...", 'red')
		return -1

	

	if(notepad.haspw):
		cprint('\nPASS: The given url is password protected', 'yellow')
	else:
		cprint("\nSaving {} to {}..... \n".format(filename,link), 'green')
		notepad.save_file(file_path, arguments['--overwrite'])



	



