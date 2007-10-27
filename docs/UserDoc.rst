#########
Npyscreen
#########

"User interfaces without all that mucking around in hyperspace"

.. contents::

Overview
========

Npyscreen is a python library that is designed to make the writing of curses-based user interfaces quick and easy.  

It is designed to run using only the python standard library, and the only requirements are a working python (2.4 or above) installation and a working curses library.  Npyscreen will therefore work on almost all common platforms, and even in the Cygwin environment on Windows.



Status of this Document
=======================

This document explains the key features of Npyscreen - enough to get you using it.  It is, however, a work in progress.


Objects Overview
================

Form Objects
	Form objects (typically the size of a whole terminal, but sometimes larger or - for menus and the like - smaller) provide an area which can contain widget objects.  They may provide additional functions like a system for handling menus, or routines that will be run if a user selects an "ok" button.  They may also define operations carried out between key-presses, or as the user moves around the Form.
	
Widget Objects
	These are the individual controls on a form - text boxes, labels, sliders, and so on.
	
Application Objects
	These objects provide a convenient way to manage the running of your application.  Although it is possible to program simple applications without using the Application objects, it is not advisable.  Application objects make the management of multiple screens much less error-prone (in the 'bugs that may at any time crash your application') sense.  In addition, making use of these objects will enable you to take advantage of additional features as npyscreen is developed.

Programming with npyscreen
==========================

Application Objects
*******************

NPSAppManaged
-------------

Unless you have exceptionally good reasons to do otherwise, this is almost certainly the best way to manage your application.  

Unlike the plain NPSApp class, you do not need to write your own main loop - NPSApp managed will manage the display of each Form of your application.  Set up your form objects and simply call the *.run()* method of your NPSAppManaged instance.

Letting NPSAppManaged manage your Forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are two methods for registering a Form object with an NPSAppManaged instance:

.registerForm(*id*, *fm*)
	*id* should be a string that uniquely identifies the form.  *fm* should be a Form object.  Note that this version only stores a weakref.proxy inside NPSAppManaged - in contrast to the .addForm version.
	
.addForm(*id*, *FormClass* ...)
	This version creates a new form and registers it with the NPSAppManaged instance.  It returns a weakref.proxy to the form object.  *id* should be a string that uniquely identifies the Form.  *FormClass* should be the class of form to create.  Any additional arguments will be passed to the Form's constructor.

All Forms registered with an NPSAppManaged instance can access the controlling application as *self.parentApp*.

If for any reason you need to remove a Form, you can do with the .removeForm(*id*) method. 

Which Form is displayed by NPSAppManaged
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once all of your forms are ready and registered with an NPSAppManaged instance, you should call .run()

This method will activate the default form, which should have been given an id of "MAIN".  You can change this default by changing the class/instance variable *.STARTING_FORM*.

Thereafter, the next form to be displayed will be the one specified by the instance variable *NEXT_ACTIVE_FORM*.  Whenever a Form edit loop exits, the Form specified here will be activated.  If *NEXT_ACTIVE_FORM* is None, the main loop will exit.

There are two mechanisms that Forms should use to control NEXT_ACTIVE_FORM.  

1. All Forms registered with an NPSAppManaged which do *not* have the special method *.activate()* will have their method *.afterEditing* called, if they have it.  Logic to determine which the *NEXT_ACTIVE_FORM* should be should go here.  This is the preferred method.

2. Forms registered with an NPSAppManaged may be given an *.activate()* method, which NPSAppManaged will call instead of the usual *.edit()* method.  This can contain additional logic.  This is NOT the preferred method, but may allow greater flexibility.  Note that in this case, the usual .edit() method will not be called, unless you call it explicitly.   For example, an .activate() method might look like this::
    
    def activate(self):
         self.edit()
         self.parentApp.NEXT_ACTIVE_FORM = None
    
   which would cause the mainloop to exit after the Form was complete.

Additional Services offered by NPSAppManaged
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following methods may be usefully overridden by subclassing NPSAppManaged.  By default they do nothing.

onInMainLoop
    Called between each screen while the application is running. Not called before the first screen. 

onStart
    Override this method to perform any initialisation.  If you wished, you could set up your application's Forms here.
        
onCleanExit
    Override this method to perform any cleanup when application is exiting without error.

NPSApp
------

To use NPSApp subclass it and provide your own .main() definition.  When you are ready to run the application call .run() and your mainloop will be executed.

While it provides maximum flexibility, NPSApp is in almost every other way inferior to NPSAppManaged.


Forms: Basic Principles
=======================

A Form object is a screen area that contains widgets.  Forms control which widget a user is editing, and may provide additional functionality, such as pop-up menus or actions that happen on particular keypresses.

Creating a Form
***************

The Following arguments can be passed to a Form's constructor:

*name=*
    Names the Form.  As for some widgets, this will display a title.

*lines=0, columns=0, minimum_lines=24, minimum_columns=80*
    You can adjust the size of the Form, either providing an absolute size (with *lines=* and *columns=*) or a minimum size (*minimum_lines=* and *minimum_columns=*).  The default miniums (24x80) provide the standard size for terminal.  If you plan your Forms to fit within that size, they should be viewable on almost all systems without the need to scroll the Form.  Note that you can use the absolute sizing in one direction and the minimum in the other, should you wish.
    
Forms cannot be resized once created.  A system to dynamically re-arrange widgets as a terminal is resized is in a experimental state but is not part of the current distribution.

The standard constructor will call the method *.create()*, which you should override to create the Form widgets.  See below.

Placing widgets on a Form
*************************

To add a widget to a Form, use the method:

*add(WidgetClass, ...)*
    WidgetClass must be a class, all of the additional arguments will be passed to the widget's own constructor.  A reference to the widget will be returned.


The position and size of a widget are controlled by the widget's constructor.  However, there are hints that the Form class provides.  If you do not override the position of the widget, it will be placed according to the Form's *.nextrelx* and *nextrely* instance attributes.  The *.nextrely* attribute is increased automatically each time a widget is placed.  You might also increase it yourself by doing something like::
   
   self.nextrely += 1

Which would leave a gap between the previous widget and the next placed one.

Other Standard Form Features
****************************

*.create()*
    This method is called by the Form's constructor.  It does nothing by default - it is there for you to override in subclasses, but it is the best place to set up all the widgets on a Form.  Expect this method to be full of *self.add(...)* method calls, then!

*.while_editing()*
    This method is called as the user moves between widgets.  It is intended for you to override in subclasses, to do things like altering one widget based on the value of another.

*adjust_widgets()*
    Be very careful with this method.  It is called for every keypress while the Form is being edited, and there is no guarantee that it might not be called even more frequently.  By default it does nothing, and is intended for you to override.  Since it gets called so frequently, thoughtlessness here could slow down your whole application.  

   For example, be very conservative with redraws of the whole Form (a slow operation) - make sure you put in code to test whether a redraw is necessary, and try to only redraw widgets that really need to be changed, rather than redrawing the whole screen.
   
*while_waiting(), keypress_timeout*
   If you wish to perform actions while waiting for the user to press a key, you may define a *while_waiting* method.  You should also set the attribute *keypress_timeout*, which is a value in ms.  Whenever waiting for input, if more than the time given in *keypress_timeout* passes, while_waiting will be called.  Note that npyscreen takes no steps to ensure that *while_waiting()* is called at exactly regular intervals, and in fact it may never be called at all if the user continually presses keys.
   
   A *keypress_timeout* value of 10 ensures that the *while_waiting* method is called about every second.
   
   See the included example TIMEOUT-EXAMPLE.py for a fully worked example.

Displaying and Editing Forms
****************************

*.display()*
    Redraw every widget on the Form and the Form itself.

*.edit()*
    Allow the user to interactively edit the value of each widget.  You should not need to call this method if correctly using the *NPSAppManaged* class, but will need to use it otherwise.

Form Classes
============

Form, Popup
   The basic Form class.  When editing the form, the user can exit by selecting the OK button in the bottom right corner.
   
   By default, a Form will fill the Terminal.  Popup is simply a Form with a smaller default size.
   
ActionForm, ActionPopup
   The ActionForm creates OK and Cancel buttons.  Selecting either exits the form.  The method *on_ok* or *on_cancel* is called when the Form exits.  Subclasses may therefore usefully override one or both of these methods, which by default do nothing.
   
TitleForm, TitleFooterForm, SplitForm
   These are Form classes with slightly different layouts.
   
   The SplitForm has a horizontal line across the middle.  The method *get_half_way()* will tell you where it has been drawn.
   
FormWithMenus, ActionFormWithMenus
   These forms are similar to the Form and ActionForm classes, but provide the additional functionality of Popup menus.
   
   To add a new menu to the Form use the method *new_menu(name='')*.  This will create the menu and return a proxy to it.  For more details see the section on Menus below.
   
Menus
=====

Some Form classes support the use of popup menus.  Indeed, menus could in theory be used as widgets on their own.  Popup menus (inspired, in fact, by the menu system in RiscOS) were selected instead of drop-down menus as being more suitable for a keyboard environment, making better use of available screen space and being easier to deploy on terminals of varied sizes.

Menus are usually created by calling a (supporting) Form's *new_menu* method.  Thereafter, the following methods are useful:

*addItem(text='', onSelect=function)*
   *text* should be the string to be menu.  onSelect should be a function to be called if that item is selected by the user.  This is one of the few easy opportunities in npyscreen to create circular references - you may wish to pass in a proxy to a function instead.  I've tried to guard you against circular references as much as possible - but this is just one of those times I can't second-guess your application structure.
   
*addNewSubmenu(...)*
   Create a new submenu (returning a proxy to it).  This is the preferred way of creating submenus. 
   
*addSubmenu(submenu)*
    Add an existing Menu to the Menu as a submenu.  All things considered, addNewSubmenu is usually a better bet.

    
(Internally, this menu system is referred to as the "New" menu system - it replaces a drop-down menu system with which I was never very happy.)



Widgets: Basic Features
=======================

Widgets are created by passing their class as the first argument of a Form's *add(...)* method.  The remaining arguments will be passed to the widget's own constructor.  These control things such as size, position, name, and initial values.

Constructor arguments
*********************

*name=*
  You should probably give each widget a name (a string).  Where appropriate, it will be used as the label of the widget.

*relx=*, *rely=*
   The position of the widget on the Form is controlled by relx and rely integers.   You don't have to specify them, in which case the form will do its best to decide where to put the widget.  You can specify only one or the other if you so choose (eg. you probably don't usually need to specify relx).

*width=*, *height=*, *max_width=*, *max_height=*
   By default, widgets will expand to fill all available space to the right and downwards, unless that would not make sense - for example single lines of text do not need moe than one line, and so don't claim more than one.  To alter the size of a widget, therefore, specify a different *max_width* or *max_height*.  It is probably better to use the max\_ versions - these will not raise an error if space is getting tight and you specify too much, but will try to squash the widget into remaining space.

*value=*
   The value of a widget is the thing a user can change - a string, a date, a selection of items, a filename.  The initial setting of the *.value* attribute can be specified here.

*values=*
   Where a widget offers the user a selection from a list of values, these can be specified here: this is the initial setting of the *values* attribute.

*editable=True*
   Whether the user should be able to edit a widget.  (Initial setting of the *.editable* attribute.)

*hidden=False*
   Whether a widget is visible or not.  (Initial setting of the *.hidden* attribute.)

*color='DEFAULT'*, labelColor='LABEL'
   Provides a hint to the colour-management system as to how the widget should be displayed.  More details elsewhere.
   
*scroll_exit=False*, *slow_scroll=False*, *exit_left*, *exit_right*
    These affect the way a user interacts with multi-line widgets.  *scroll_exit* decides whether or not the user can move from the first or last item to the previous or next widget.  *slow_scroll* means that widgets that scroll will do so one line at at time, not by the screen-full. The options *exit_left|right* dictate whether the user can exit a widget using the left and right arrow keys.

Using and Displaying Widgets
****************************

All widgets have the following methods:

*display()*
   Redraws the widget and tells curses to update the screen.

*update()*
   Redraws the widget, but doesn't tell curses to update the screen (it is more efficient to update all widgets and then have the Form on which they sit tell curses to redraw the screen all in one go).

   Most widgets accept the optional argument *clear=False|True* which affects whether they first blank the area they occupy before redrawing themselves

*edit()*
   Allow the user to interact with the widget.  The method returns when the user leaves the widget.

Titled Widgets
**************

Many widgets exist in two forms, one with a label, one without.  For example Textbox and TitleText.  If the label is particularly long (at time of construction), the label may be put on its own line.  Additional constructor arguments:

*use_two_lines=*
  If either True or False, override what the widget would otherwise choose. 

*field_width=*
  (For text fields) - how wide should the entry part of the widget be?

*begin_entry_at=16*
   At what column should the entry part of the widget begin?

Internally titled widgets are actually a textbox (for the label) and whatever other kind of widget is required.  You can access the separate widgets (if you ever need to - you shouldn't) through the *label_widget* *entry_widget* attributes.

However, you may never need to, since the *value* and *values* attributes of the combined widget should work as expected.

Widget Types
============

Displaying Text
***************

Textbox, TitleText
   A single line of text, although of arbitrary length - the basic entry widget.

FixedText, TitleFixedText
   A single line of text, but with the editing functions of Textbox removed.

PasswordEntry, TitlePassword
   A textbox but altered so that the exact letters of *.value* are not displayed.  

Autocomplete
   This is a textbox but with additional functionality - the idea is that if the user presses TAB the widget will attempt to 'complete' what the user was typing, offering a choice of options if appropriate.  

   Of course, context is everything here.  *Autocomplete* is therefore not useful, but is intended as something you can subclass.  See the Filename and TitleFilename classes for examples. 

TitleFilename, Filename
   A textbox that will attempt to 'complete' a filename or path entered by the user.
   
   This is an example of the *Autocomplete* widget.

MultiLineEdit
   This widget allows the user to edit several lines of text. 

Pager
   This widget displays lines of text, allowing the user to scroll through them, but not edit them.



Picking Options
***************

MultiLine
   Offer the user a list of options.  (This widget could probably have a better name, but we're stuck with it for now)

   The options should be stored in the attribute *values* as a list.  The attribute *value* stores the index of the user's selection.

   One of the most important features of MultiLine and widgets derived from it is that it can be adapted easily to allow the user to choose different types of objects.  To do so, override the method *display_value(self, vl)*.  The argument *vl* will be the object being displayed, and the function should return a string that can be displayed on the screen.
   
   MultiLine also allows the user to 'filter' entries.  (bound to keys l, L, n, p by default for filter, clear filter, next and previous). The current implementation highlights lines that match on the screen.  Future implementations may hide the other lines or offer a choice.  You can control how the filter operates by overriding the filter_value method.  This should accept an index as an argument (which looks up a line in the list .values) and should return True on a match and False otherwise.

TitleMultiLine
   A titled version of the MultiLine widget.  

   If creating your own subclasses of MultiLine, you can create Title versions by subclassing this object and changing the _entry_type class variable.

MultiSelect, TitleMultiSelect, 
    Offer the User a list of options, allow him or her to select more than one of them.
    
    The *value* attribute is a list of the indexes user's choices.  As with the MultiLine widget, the list of choices is stored in the attribue *values*.

SelectOne, TitleSelectOne
    Functionally, these are like the Multiline versions, but with a display similar to the MultiSelect widget.

MultiSelectFixed, TitleMultiSelectFixed
    These special versions of MultiSelect are intended to display data, but like Textfixed do not allow the user to actually edit it.

Dates, Sliders and Combination Widgets
**************************************

DateCombo, TitleDateCombo
    These widgets allow a user to select a date.  The actual selection of a date is done with the class MonthBox, which is displayed in a temporary window.

ComboBox, TitleCombo
    This box looks like a Textbox, but the user can only select from a list of options.  Which are displayed in a temporary window if the user wants to change the value.  Like the MultiLine widget, the attribute *value* is the index of a selection in the list *values*.  The ComboBox widget can also be customised by overloading the *display_value(self, vl)* method. 

Slider, TitleSlider
   Slider presents a horizontal slider.  The following additional arguments to the constructor are useful:

   out_of=100
      The maximum value of the slider.
   step=1
      The increments by which a user my increase or decrease the value.
   lowest=0
      The minimum value a user can select. Note that sliders are not designed to allow a user to select negative values.  *lowest* should be >= 0
   label=True
      Whether to print a text label next to the slider.  If so, see the *translate_value* method.
      
   All of these options set attributes of the same name that may be altered once the widget exists.
   
   The text displayed next to the widget (if *label=True*) is generated by the *translate_value* method.  This takes no options and returns a string.  It makes sense to subclass the Slider object and overload this method.  It probably makes sense to ensure that the string generated is of a fixed length.  Thus the default code looks like::
   
      stri = "%s / %s" %(self.value, self.out_of)
      l = (len(str(self.out_of)))*2+4
      stri = stri.rjust(l)
      return stri

Trees and Tree displays
***********************
(The tree objects are the newest part of the library, and are therefore not as mature as the rest of it. In particular, the exact way they are displayed may change in future versions.).



NPSTreeData
    The NPSTreeData class is used to represent tree objects.  Each nod of the tree, including the root node, is an NPSTreeData instance.  Each node may have its own content, a parent or children.

    The content of each node is either set when it is created or using the *.setContent* method.

    *.getContent* returns the content.

    *.getContentForDisplay* is used by the widgets that display trees, which expect it to return a string that can be displayed to the user to represent the content.  You might want to overload this method.

    *newChild(content=...)* creates a new child node.
    
Widgets
~~~~~~~
MultiLineTree, SelectOneTree, and MultiLineTree
    These widgets all work in a very similar way to the non-Tree versions, except that they expect to contain an NPSTree in their .values attribute.  The other major difference is that their .value attribute does not contain the index of the selected value(s), but the selected value(s) itself/themselves.


Other Controls
**************

Checkbox, RoundCheckBox
   These offer a single option - the label is generated from the attribute *name*, as for titled widgets.  The attribute *value* is either true or false.


Button
   Functionally similar to the Checkbox widgets, but looking different.  The Button is usually used for OK and Cancel Buttons on Forms and similar things.
   
FormControlCheckbox
   A common use of Checkbox is to offer the user the option to enter additional data.  For example "Enter Expiry Date".  In such a case, the Form needs to display additional fields in some cases, but not in others.  FormControlCheckbox makes this trivial.
   
   Two methods are defined:
   
   addVisibleWhenSelected(*wg*)
      *wg* should be a widget.  
      
      This method does not create a widget, but instead puts an existing widget under the control of the FormControlCheckbox.  If FormControlCheckbox is selected, the widget will be visible.  
      
      As many widgets as you wish can be added in this way.
      
   addInvisibleWhenSelected(*wg*)
      Widgets registered in this way are visible only when the FormControlCheckbox is not selected.
      



    
All about Key Bindings
======================

What's going on
***************

Many objects can take actions based on user key presses.  All such objects inherit from the internal class InputHandler.  That class defines a dictionary called *handlers* and a list called *complex_handlers*.  Both of these are set up by a method called set_up_handlers called during the Constructor.

*handlers*
   Might look something like this::
   
        {curses.ascii.NL:   self.h_exit_down,
         curses.ascii.CR:   self.h_exit_down,
         curses.ascii.TAB:  self.h_exit_down,
         curses.KEY_DOWN:   self.h_exit_down,
         curses.KEY_UP:     self.h_exit_up,
         curses.KEY_LEFT:   self.h_exit_left,
         curses.KEY_RIGHT:  self.h_exit_right,
         "^P":		        self.h_exit_up,
         "^N":		        self.h_exit_down,
         curses.ascii.ESC:	self.h_exit_escape,
         curses.KEY_MOUSE:	self.h_exit_mouse,
         }

    If a key is pressed (note support for notations like "^N" for "Control-N" and "!a" for "Alt N") that exists as a key in this dictionary, the function associated with it is called.  No further action is taken.  By convention functions that handle user input are prefixed with h\_.

*complex_handlers*
    This list should contain list or tuple pairs like this (test_func, dispatch_func).  
    
    If the key is not named in the dictionary *handlers*, each test_func is run.  If it returns True, the dispatch_func is run and the search stops.
    
    Complex handlers are used, for example, to ensure that only printable characters are entered into a textbox.  Since they will be run frequently, there should be as few of them as possible, and they should execute as quickly as possible.
    
When a user is editing a widget and a key is pressed, *handlers* and then *complex_handlers* are used to try to find a function to execute.  If the widget doesn't define an action to be taken, the *handlers* and *complex_handlers* of the parent Form are then checked.

Adding your own handlers
************************

Objects that can handle user input define the following methods to assist with adding your own key bindings:

*add_handlers(new_handlers)*
    *new_handlers* should be a dictionary.

*add_complex_handlers(new_handlers)*
    *new_handlers* should be a list of lists.  Each sublist must be a pair *(test_function, callback)*

Support for Colour
==================

Setting up colour
*****************

All of the standard widgets are entirely usable on a monochrome terminal.  However, it's a colourful world these days, and npyscreen lets you display your widgets in, well, if not Technicolor(TM) then as close a curses will allow.

Colour is handled by the ThemeManager class.  Generally, your application should stick to using one ThemeManager, which you should set using the *setTheme(ThemeManager)* function.  So for example::

    npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
    
Any default themes defined by npyscreen will be accessible via npyscreen.Themes.

A basic theme looks like this::

    class DefaultTheme(npyscreen.ThemeManager):
        default_colors = {
            'DEFAULT'     : 'WHITE_BLACK',
            'FORMDEFAULT' : 'YELLOW_BLACK',
            'NO_EDIT'     : 'BLUE_BLACK',
            'STANDOUT'    : 'CYAN_BLACK',
            'LABEL'       : 'BLUE_BLACK',
            'LABELBOLD'   : 'WHITE_BLACK',
            'CONTROL'     : 'GREEN_BLACK',
        }
        
The colours - such as WHITE_BLACK ("white on black") - are defined in the *initialize_pairs* method of the ThemeManager class.  The following are defined by default::
    
    ('BLACK_WHITE',      curses.COLOR_BLACK,      curses.COLOR_WHITE),
     ('BLUE_BLACK',       curses.COLOR_BLUE,       curses.COLOR_BLACK),
     ('CYAN_BLACK',       curses.COLOR_CYAN,       curses.COLOR_BLACK),
     ('GREEN_BLACK',      curses.COLOR_GREEN,      curses.COLOR_BLACK),
     ('MAGENTA_BLACK',    curses.COLOR_MAGENTA,    curses.COLOR_BLACK),
     ('RED_BLACK',        curses.COLOR_RED,        curses.COLOR_BLACK),
     ('YELLOW_BLACK',     curses.COLOR_YELLOW,     curses.COLOR_BLACK),
    )

('WHITE_BLACK' is always defined.)    

If you find you need more, subclass ThemeManager and change class attribute *_colours_to_define*.   You are able to use colours other than the standard curses ones, but since not all terminals support doing so, npyscreen does not by default.

If you want to disable all colour in your application, npyscreen defines two convenient functions: *disableColor()* and *enableColor()*.

How Widgets use colour
**********************

When a widget is being drawn, it asks the active ThemeManager to tell it appropriate colours.  'LABEL', for example, is a label given to colours that will be used for the labels of widgets.  The Theme manager looks up the relevant name in its *default_colors* dictionary and returns the appropriate colour-pair as an curses attribute that is then used to draw the widget on the screen.

Individual widgets often have *color* attribute of their own (which may be set by the constructor).  This is usually set to 'DEFAULT', but could be changed to any other defined name.  This mechanism typically only allows individual widgets to have one particular part of their colour-scheme changed.

Title... versions of widgets also define the attribute *labelColor*, which can be used to change the colour of their label colour.

