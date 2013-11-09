#!/usr/bin/env python
from distutils.core import setup

setup(
	name="npyscreen",
	version="2.0pre82",
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

Please report bugs or make feature requests using the bug-tracker at http://code.google.com/p/npyscreen.

There is a mailing list available at https://groups.google.com/forum/?fromgroups#!forum/npyscreen/


*Latest Changes*:
Version 2.0pre82 changes the menu system and allows menu items to be given keyboard shortcuts.

Version 2.0pre81 introduces FilenameCombo, TitleFilenameCombo.

Version 2.0pre79 is a bugfix release.

Version 2.0pre76 further improves the handling of mouse events on compatible
terminals.


Version 2.0pre75 improves the handling of the mouse on compatible terminals.

Version 2.0pre74 corrects one minor bug and introduces makes box widgets
behave slightly more predictably (.editable attribute now linked to that of
the contained widget.

Version 2.0pre73 corrects two bugs - thanks to Lasse for his help in finding
them and offering patches.

Version 2.0pre71 new tree classes introduced. Bug fixes.

Version 2.0pre70 introduces the MLTreeMultiSelect class.

Version 2.0pre69 fixes and tidies up some of the new tree classes.  There is an API change assocatied with this, noted in the documentation, though backward compatibility should have been maintained. 

Version 2.0pre68 setting a form's .editing attribute to False now causes it to exit immediately,
even if a widget is still being edited.

Version 2.0pre67 fixes minor bugs.

Version 2.0pre65 fixes several bugs.  All textboxes now honour the .hidden
attribute.  The major side effect of this is that tree classes are now
easier to write.

Version 2.0pre64 extends multi-page support and includes revision to the
documentation.

Version 2.0pre63 adds initial support for multi-page forms.  See documentation on the 
FormMultiPage class for details.

Version 2.0pre57 fixes color support - it should now be possible to display
a terminal with a different color background. Text widgets have some
additional color options.

Version 2.0pre52 fixes compatibility with python2.6, 3.0 and 3.1.  All other versions should be unaffected.

Version 2.0pre50 enables basic mouse support.  Note that the Apple terminal does not handle mouse events correctly.
"""
)
