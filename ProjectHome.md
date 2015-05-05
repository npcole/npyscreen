**Npyscreen is a python widget library and application framework for programming terminal or console applications.  It is built on top of ncurses, which is part of the standard library.**

# Documentation #

Online documentation can be found at:

http://npyscreen.readthedocs.org/

## Downloads ##

The library can be downloaded from:

https://pypi.python.org/pypi/npyscreen/

# Strengths #

This framework should be powerful enough to create everything from quick, simple programs to complex, multi-screen applications. It is designed to make doing the simple tasks very quick and to take much of the pain out of writing larger applications.

There is a very wide variety of default widgets - everything from simple text fields to more complex tree and grid views.

The framework is easy to extend. That said, if you have a requirement for a widget that is not currently included you can try emailing me and I'll see whether I have time to help - no promises!

# Support #

Please use the Issue Tracker on this page to report bugs and other problems, or to make feature requests.

There is a mailing list at https://groups.google.com/forum/?fromgroups#!forum/npyscreen/ if you need help getting your application to run.


---


## Non-English Text ##

From version 2.0pre47 onwards all text widgets should now support utf-8 text display and entry on utf-8 capable terminals.  This fixes a long-standing limitation with the library, and makes it suitable for use in projects targeting non-English-speaking users.

As of version 2.0pre48, the library aims to be robust in dealing with unicode across all widgets.  There are still a few places in the system where support for utf-8/unicode needs further work. Please file bug reports if you encounter them.

The 2.0pre48 release should be considered an alpha-release for version 2.

## Recent Improvements ##
Version 2.0pre88 introduces support for resizing the Terminal.  This removes a long-standing limitation. Please report any problems.

Version 2.0pre83 introduces support for multi-line checkbox widgets.

Version 2.0pre69 cleans up the tree classes, in preparation for future improvements.

Version 2.0pre63 adds preliminary support for multipage forms. This is an experimental feature.

From version 2.0pre50 onwards the mouse can be used.  Prior to version 2.0pre50 the library did not support the mouse, mostly because I had not had the need for mouse support.  In the most recent versions, the mouse is used simply to switch the focus between widgets, but it is trivial to add more detailed functionality.  Note that on OS X, Terminal.App does not correctly pass mouse events to curses, but xterm does.

Prior to version 2.0pre47, support for unicode was limited. Current versions support unicode on all text widgets and their derived classes.  However, because python currently provides no reliable way to guess the width of a character, support for multi-width characters is still not available. I hope to find a work-around in a future release.


## Python 3 support ##

From version 2.0pre31 onwards this library should work on python 3, though some of the internals have been rewritten.  The public api is unchanged, and the new code continues to work on python 2.  I am currently still using python 2 for development.  All future versions will target both python 2 and 3, unless a feature unique to python 3 becomes vital.

## Similar Projects ##

You might also like to look at http://excess.org/urwid/

Compared to npyscreen, urwid is more like a traditional, event-driven gui library, and targets other display devices as well as curses.