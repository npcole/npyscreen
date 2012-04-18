#!/usr/bin/env python
from distutils.core import setup

setup(
	name="npyscreen",
	version="2.0pre52",
	description="Writing user interfaces without all that ugly mucking about in hyperspace",
	author="Nicholas Cole",
	author_email="n@npcole.com",
	url="http://www.npcole.com/npyscreen/",
	packages=['npyscreen'],
	license='New BSD License',
	classifiers= [
	    'Development Status :: 5 - Production/Stable',
	    'Programming Language :: Python :: 3',
	    'Programming Language :: Python :: 2.6',
	    'Programming Language :: Python :: 2.7',
	    'Environment :: Console',
	    'Operating System :: POSIX',
	    'Environment :: Console :: Curses',
	    'Intended Audience :: Developers',
	    'License :: OSI Approved :: BSD License',
	    'Topic :: Terminals'
	    ],
	long_description = """This library provides a framework for developing console applications using Python and curses.

This framework should be powerful enough to create everything from quick, simple programs to complex, multi-screen applications. It is designed to make doing the simple tasks very quick and to take much of the pain out of writing larger applications.

There is a very wide variety of default widgets - everything from simple text fields to more complex tree and grid views.

I have used versions of this library for private scripts and small applications for around ten years. As a result, it is fairly mature.	

Please report bugs using the bug-tracker at http://code.google.com/p/npyscreen.

*Latest Changes*:
Version 2.0pre52 fixes compatibility with python2.6, 3.0 and 3.1.  All other versions should be unaffected.

Version 2.0pre50 enables basic mouse support.  Note that the Apple terminal does not handle mouse events correctly.
"""
)
