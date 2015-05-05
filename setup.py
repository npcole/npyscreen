#!/usr/bin/env python
from distutils.core import setup

setup(
	name="npyscreen",
	version="4.8.7",
	description="Writing user interfaces without all that ugly mucking about in hyperspace",
	author="Nicholas Cole",
	author_email="n@npcole.com",
	url="http://www.npcole.com/npyscreen/",
	packages=['npyscreen', 'npyscreen.compatibility_code'],
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

Documentation is online at http://npyscreen.readthedocs.org

Please report bugs or make feature requests using the bug-tracker at http://code.google.com/p/npyscreen.

There is a mailing list available at https://groups.google.com/forum/?fromgroups#!forum/npyscreen/


*Latest Changes*:
Version 4.8.7 New methods added to the Multiline class to assist widget authors. 


Version 4.8.6 MultiLineAction widgets no longer raise an exception if empty
and selected unless set to do so explicitly.

Version 4.8.5 improves the writing of tests.

Version 4.8.4 adds support for custom-defined colours (not recommended.
Added at user request for a custom application).

Version 4.8.3 updates the documentation.

Version 4.8.2 makes the standard grid widget easier to customize by adding
the custom_print_cell method.

Version 4.8.1 fixes a bug that causes npyscreen to crash.

Version 4.8.0 adds a mechanism for finer control of BoxTitle contained
widgets.

Version 4.7.2 includes documentation updates.

Version 4.7.1 is a bugfix release.

Version 4.7.0 adds scripting support for writing automated tests.

Version 4.6.4 adds keybindings relevant to Windows.

Version 4.6.3 is a minor bug-fix release.

Version 4.6.1 updates the documentation to note that there is a bug in
Python's curses library in 3.4.0.  This is fixed in 3.4.1.  I do not propose
to put a workaround into npyscreen, which would complicate the code a great
deal for a bug that very few people face.  For more details, see:
http://bugs.python.org/issue21088




Version 4.6.0 introduces a way to define a callback for when widget values change.  The help system has been improved by minor interface changes.  
Both of these were user suggestions.  Thank you to those who suggested them.

Version 4.5.0 introduces a greater control of colour for certain widgets.  

Version 4.4.0 introduces the new tree class TreeData.  This is a new version of NPSTreeData that follows PEP 8 conventions for method names.  NPSTreeData is now deprecated.
The form class ActionFormMinimal has been added at a user request.  This is a special version of ActionFrom that only features an OK button by default.

Version 4.3.5 introduces the new classes SliderNoLabel, TitleSliderNoLabel, SliderPercent, TitleSliderPercent.


Version 4.3.4 Minor bugfixes.  The notify functions and ActionPopups derived from them now use the ActionFormV2 widgets.  
This change should not affect existing code, but let me know if there are problems.

Version 4.3.0 allows you to specify a negative value for rely or relx when creating a widget.  This will cause the widget to be aligned
with the bottom or right of the screen.  The new method *set_relyx(y, x)* can be used to set the position of the widget on the Form if you never need to do that manually. 

The classes *ActionFormV2*, *ActionFormExpandedV2* and *ActionFormV2WithMenus* have been introduced.
These feature cleaner code that should be easier to subclass.  

The *ButtonPress* class can now be created with the argument
*when_pressed_function=None*, which can be used in place of overriding the *whenPressed* method.  Note that this might create a reference cycle
within your application, so use with care. 


Version 4.2.0 introduces the ability of Grid widgets to highlight the whole line that the cursor is on (user request).

Version 4.1.0 introduces support for hvc consoles (thanks to wu.fuheng@********* for the bug report).  Title widgets can now define a when_cursor_moved() method directly 
on themselves that will be called as expected by the contained entry_widget during its edit loop (user request). 


Version 4.0.0 introduces a new version scheme.  Due to a packaging error in
the 3.0 release series some users were having problems obtaining the latest
version. This is most easily fixed with a new major version release.

Version 3.10 MultiLineEditable, MultiLineEditableTitle, MultiLineEditableBoxed classes added, allowing the user to edit lists of items. 
See EXAMPLE-MultilineEditable for an example.   

Version 3.6 Title.. widgets should now resize properly.  Menu items can now
be specified with arguments and keywords.

Version 3.5 when_value_edited defined on Title.. widgets now work as users expect.

Version 3.4 Fixed bugs in Title.. widgets and in the App classes.

Version 3.3 and the subsequent minor releases fix some bugs, mainly related
to changes caused by allowing resized forms.

Version 3.2 adds CheckboxBare - a checkbox without a label.  Added at user request. 

Version 3.0 *IMPORTANT* The version number has changed to version 3.0.  
This is because newer versions of pip distinguish between pre-release and released versions, 
and this will allow more flexibility in future releases. A version '2.0' might have caused confusion at this stage.  

Version 3.0 fixes the specification of max_width values for titled widgets (Thanks to Phil Rich for the bug report).  
Please report any further problems.

Version 2.0pre90 introduces a new BufferPager and TitleBufferPager class. (User request, suggested by dennis@wsec.be)

Version 2.0pre88 *IMPORTANT* This version supports resizing the terminal.
Read the documentation for more detail about how to disable this feature if
you need to.  It has been implemented in a way that should be compatible
with existing code.  New code can make the resizing even more flexible.

Version 2.0pre87 Updates the documentation and contains various bug fixes.

Version 2.0pre85 and 2.0pre86 are both bugfix releases. 

Version 2.0pre84 introduces an experimental system for editing lists of
options.  See documentation for details.

Version 2.0pre83 multi-line checkbox widgets are now possible.  These can also be used as contained widgets within the multiselect class. See documentation for details.

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
