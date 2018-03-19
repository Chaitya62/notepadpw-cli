#!/usr/bin/env python3
"""
Notepad.pw CLI

Usage: 	
	npw [options] FILE LINK
	npw [-g] LINK FILE


Example:
	npw -lo test.py testingthiscli

Options:
	-h, --help		Show this screen
	--version       	Show version
	-l, --live-update   	Enable live update on notepad
	-o, --overwrite     	Overwrite notepad contents
	-w ,--watch         	Watch file for changes 
	-g        	   	Copy contents of pad to a file

Note: Watch mode will overwrite contents of the notepad

"""

import os
import time

from docopt import docopt
from termcolor import cprint


from npwcli.update_content import Notepad
from npwcli import __version__




WARNING = 'red'
MESSAGE = 'blue'
SUCCESS = 'green'




def start():


	arguments = docopt(__doc__, version='npw version '+'.'.join(str(i) for i in __version__))
	

	filename = arguments.get('FILE', None)
	curr_dir = os.getcwd()
	file_path = os.path.join(curr_dir, filename)


	live_update = arguments.get('--live-update', False)
	watch = arguments.get('--watch', False)

	get= arguments.get('-g', False)



	link = arguments.get('LINK', None)


	try: 

		cprint('Connecting to notepad.pw....',MESSAGE)

		notepad = Notepad(link, live_update=live_update)

	except Exception as e:

		cprint("\nError: Something went wrong...", WARNING)
		return -1

	

	if(get):
		notepad.save_to_file(filename, True)
		cprint("Saved contests of {} to {} succesfully".format(link, filename), SUCCESS)
		return 1;




	if(notepad.haspw):
		cprint('\nPASS: The given url is password protected', MESSAGE)
	else:
		cprint("Saving {} to {}..... \n".format(filename,link), SUCCESS)
		notepad.save_file(file_path, arguments['--overwrite'])

		try:

			if watch:
				cprint('Watching {} for changes'.format(filename),MESSAGE)

			while watch:
				time.sleep(5)
				if notepad.is_file_content_changed():
					cprint('\nChanges detected', MESSAGE)
					notepad.save_file(file_path, True)
					cprint('Changes saved',MESSAGE)

		except  KeyboardInterrupt:

			cprint('\nClosing npw', MESSAGE) 


	



