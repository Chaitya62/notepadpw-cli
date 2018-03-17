
try:

	from setuptools import setup
except:
	from distutils.core import setup


dependencies = ['docopt', 'termcolor']


setup(
	name='npwcli',
	version='0.0.1',
	description='A notepad.pw magician in your command line',
	url='https://github.com/Chaitya62/notepadpw-cli',
	author='Chaitya Shah',
	author_email='chaitya.shah@somaiya.edu',
	install_requires=[],
	packages=['npwcli'],
	entry_points={
		'console_scripts': {
			'npw=npwcli.cli:start'
		}
	},
	classifiers={
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.5'

	}
	) 


