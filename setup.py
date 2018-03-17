from npwcli import __version__

import os
import sys

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup


dependencies = ['docopt', 'termcolor', 'socketIO_client', 'brotli']


def publish():
	os.system("python3 setup.py sdist upload")



if sys.argv[-1] == "publish":
	publish()
	sys.exit()


setup(
	name='npw',
	version='.'.join(str(i) for i in __version__),
	description='A notepad.pw magician in your command line',
	url='https://github.com/Chaitya62/notepadpw-cli',
	author='Chaitya Shah',
	author_email='chaitya.shah@somaiya.edu',
	install_requires=dependencies,
	packages=['npwcli'],
	entry_points={
		'console_scripts': [
			'npw=npwcli.cli:start'
		]
	},
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'Programming Language :: Python',
	]
	) 


