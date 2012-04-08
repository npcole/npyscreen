#!/usr/bin/env python
from distutils.core import setup

setup(
	name="npyscreen",
	version="2.0pre48",
	description="Writing user interfaces without all that ugly mucking about in hyperspace",
	author="Nicholas Cole",
	author_email="n@npcole.com",
	url="http://www.npcole.com/npyscreen/",
	packages=['npyscreen'],
	license='New BSD License',
	classifiers= [
	    'Environment :: Console',
	    'Operating System :: POSIX',
	    'Environment :: Console :: Curses',
	    'Intended Audience :: Developers',
	    'License :: OSI Approved :: BSD License',
	    'Topic :: Terminals'
	    ]   
)
