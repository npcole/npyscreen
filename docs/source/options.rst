Application Support
===================

Options and Option Lists
************************

One common problem is to display a list of options to the user.  In simple applications, a custom designed form may be used for this purpose, but for many tasks an automatically generated form is desirable.  An *experimental* system to support this was introduced in version 2.0pre84.  

At the core of this system is the concept of the *Option* object.  These objects store either single values or lists of values depending on their type, as well as any documentation that goes with the option in question and which should be presented to the user.  Options are created with the following arguments: *OptionType(name, value=None, documentation=None, short_explanation=None, option_widget_keywords = None, default = None)*.  The *short_explanation* argument is currently not used by the default widgets but will be used in future versions.  Option classes designed to allow the user to select from a limited range of options may also be created with the *choices* arguement. 

All option classes also have the class attributes DEFAULT and WIDGET_TO_USE.  The first of these defines a default value if this is not specified.  The second specifies the class of widget that is used to allow the user to adjust the option in question.

The following option classes are currently defined: `OptionFreeText`, `OptionSingleChoice`, `OptionMultiChoice`, `OptionMultiFreeList`, `OptionBoolean`, `OptionFilename`, `OptionDate`, `OptionMultiFreeText`.  The value stored in the Option object should be set with the *set(value)* method and retrieved with the *get()* method.  All Option classes also define a method *when_set* which can be overridden and which will be called after the value is changed.  Options that allow the user to select from a series of limited choices also have the methods *setChoices(choices)* and *getChoices*.

An option list can be displayed using the *OptionListDisplay* widget.  This takes a list of options as its *values* attribute.  If an option is selected, a form will be presented to the user that will display the documentation (if any) and allow the user to change the value of it. 

Option collections may be gathered together with an *OptionList* object.  *OptionList* classes have an attribute *options*.  This is simply a list, to which Option objects may be appended. Future versions may define a different API.  The purpose of *OptionList* objects is to help saving and restoring collections of objects to test files.  The format of these files is a custom text format, similar to standard unix file but capable of storing and restoring lists of strings (using tab characters as a seperator.)  This format is still evolving, and may be changed in future versions.  Only values that vary from the default are stored. 

*OptionList* objects may be created with a *filename* argument, and have the methods *write_to_file(fn=None)* and *reload_from_file(fn=None)*.

The class *SimpleOptionForm* is a form designed to show how these elements work.  The *OptionListDisplay* widget is created as an attribute with the name *wOptionList*.

Example Code
************

The following short demo program will store the specified options in the file '/tmp/test' between invocations::

	#!/usr/bin/env python
	# encoding: utf-8

	import npyscreen
	class TestApp(npyscreen.NPSApp):
	    def main(self):
	        Options = npyscreen.OptionList()
    
	        # just for convenience so we don't have to keep writing Options.options
	        options = Options.options
    
	        options.append(npyscreen.OptionFreeText('FreeText', value='', documentation="This is some documentation."))
	        options.append(npyscreen.OptionMultiChoice('Multichoice', choices=['Choice 1', 'Choice 2', 'Choice 3']))
	        options.append(npyscreen.OptionFilename('Filename', ))
	        options.append(npyscreen.OptionDate('Date', ))
	        options.append(npyscreen.OptionMultiFreeText('Multiline Text', value=''))
	        options.append(npyscreen.OptionMultiFreeList('Multiline List'))
    
			try:
	        	Options.reload_from_file('/tmp/test')        
    		except FileNotFoundError:
				pass
				
	        F  = npyscreen.Form(name = "Welcome to Npyscreen",)

	        ms = F.add(npyscreen.OptionListDisplay, name="Option List", 
	                values = options, 
	                scroll_exit=True,
	                max_height=None)
    
	        F.edit()
    
	        Options.write_to_file('/tmp/test')

	if __name__ == "__main__":
	    App = TestApp()
	    App.run()   
