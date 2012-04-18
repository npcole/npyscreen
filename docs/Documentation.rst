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

Example Code::

    import npyscreen

    class MyTestApp(npyscreen.NPSAppManaged):
        def onStart(self):
            self.registerForm("MAIN", MainForm())
    
    class MainForm(npyscreen.Form):
        def create(self):
            self.add(npyscreen.TitleText, name = "Text:", value= "Press Escape to quit application" )
            self.how_exited_handers[npyscreen.widget.EXITED_ESCAPE]  = self.exit_application    

        def exit_application(self):
            self.parentApp.NEXT_ACTIVE_FORM = None
            self.editing = False

    def main():
        TA = MyTestApp()
        TA.run()


    if __name__ == '__main__':
        main()


NPSAppManaged
-------------

NPSAppManaged provides a framework to start and end your application and to manage the display of the various Forms that you have created, in a way that should not create recursion depth problems.

Unless you have exceptionally good reasons to do otherwise, *NPSAppManaged* is almost certainly the best way to manage your application.  

Unlike the plain NPSApp class, you do not need to write your own main loop - *NPSAppManaged* will manage the display of each Form of your application.  Set up your form objects and simply call the *.run()* method of your NPSAppManaged instance.

Letting NPSAppManaged manage your Forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are two methods for registering a Form object with an NPSAppManaged instance:

.registerForm(*id*, *fm*)
    *id* should be a string that uniquely identifies the form.  *fm* should be a Form object.  Note that this version only stores a weakref.proxy inside NPSAppManaged - in contrast to the .addForm version.
    
.addForm(*id*, *FormClass* ...)
    This version creates a new form and registers it with the NPSAppManaged instance.  It returns a weakref.proxy to the form object.  *id* should be a string that uniquely identifies the Form.  *FormClass* should be the class of form to create.  Any additional arguments will be passed to the Form's constructor.  In most cases, you should use the *registerForm* method and not this one.

.addFormClass(*id*, *FormClass* ...):
    This version registers a class of form rather than an instance.  A new instance will be created every time it is edited.

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

onInMainLoop()
    Called between each screen while the application is running. Not called before the first screen. 

onStart()
    Override this method to perform any initialisation.  If you wish, you can set up your application's Forms here.
        
onCleanExit()
    Override this method to perform any cleanup when application is exiting without error.
    
Forms called by NPSAppManaged can be given the methods

beforeEditing()
    called before the edit loop of the form is called

afterEditing()
    called when the form is exited

activate()
    The presence of this method entirely overrides the existing .beforeEditing .edit  and afterEditing methods.
    
switchForm(formid)
    Immediately stop editing the current form and switch to the specified form.

The following attribute affects new Forms:

keypress_timeout_default
    If this is set, new forms will be created with keypress_timeout set to this, provided they know what application they belong to - i.e. they have been passed *parentApp=* at creation time. If you are using NPSAppManaged, this will happen automatically.

*while_waiting()*, *_internal_while_waiting()*
    Applications can also have a *while_waiting* method.  You can define and override this at will, and it will be called while the application is waiting for user input (see the while_waiting method on forms).  The *_internal_while_waiting()* method is for internal use by npyscreen.

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
    You can adjust the size of the Form, either providing an absolute size (with *lines=* and *columns=*) or a minimum size (*minimum_lines=* and *minimum_columns=*).  The default minimums (24x80) provide the standard size for terminal.  If you plan your Forms to fit within that size, they should be viewable on almost all systems without the need to scroll the Form.  Note that you can use the absolute sizing in one direction and the minimum in the other, should you wish.
    
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
   
   A *keypress_timeout* value of 10 suggests that the *while_waiting* method is called about every second, assuming the user takes no other action.
   
   See the included example Example-waiting.py for a fully worked example.
   
*set_value(value)*
    Store *value* in the *.value* attribute of the *Form* and then call the *whenParentChangeValue* method of every widget that has it.

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
   
   All form classes can have the method *set_value(value)*.  This sets the value of the attribute *value* and calls the method *when_parent_changes_value* of every contained widget on the form.
   
ActionForm, ActionPopup
   The ActionForm creates OK and Cancel buttons.  Selecting either exits the form.  The method *on_ok* or *on_cancel* is called when the Form exits.  Subclasses may therefore usefully override one or both of these methods, which by default do nothing.
   
TitleForm, TitleFooterForm, SplitForm
   These are Form classes with slightly different layouts.
   
   The SplitForm has a horizontal line across the middle.  The method *get_half_way()* will tell you where it has been drawn.
   
FormWithMenus, ActionFormWithMenus
   These forms are similar to the Form and ActionForm classes, but provide the additional functionality of Popup menus.
   
   To add a new menu to the Form use the method *new_menu(name='')*.  This will create the menu and return a proxy to it.  For more details see the section on Menus below.
   
FormBaseNew, FormBaseNewWithMenus
    This form does not have an *ok* or *cancel* button by default.  The additional methods *pre_edit_loop* and *post_edit_loop* are called before and after the Form is edited.  The default versions do nothing.  This class is intended as a base for more complex user interfaces.
    
FormMutt
    Inspired by the user interfaces of programs like *mutt* or *irssi*, this form defines four default widgets:
    
    *wStatus1*
        This is at the top of the screen.  You can change the type of widget used by changing the *STATUS_WIDGET_CLASS* class attribute (note this is used for both status lines).
    *wStatus2*
        This occupies the second to last line of the screen. You can change the type of widget used by changing the *STATUS_WIDGET_CLASS* class attribute (note this is used for both status lines).
    *wMain*
        This occupies the area between wStatus1 and wStatus2, and is a MultiLine widget.  You can alter the type of widget that appears here by subclassing *FormMutt* and changing the *MAIN_WIDGET_CLASS* class attribute.
    *wCommand*
        This Field occupies the last line of the screen. You can change the type of widget used by altering the *COMMAND_WIDGET_CLASS* class attribute.
   
    By default, wStatus1 and wStatus2 have *editable* set to False.
    
FormMuttActive
    This class is intended to make the creation of more complicated applications easier.  It uses the additional classes *NPSFilteredDataBase* and *ActionControllerSimple* 
    
    
Menus
=====

Some Form classes support the use of popup menus.  Menus could in theory be used as widgets on their own.  Popup menus (inspired, in fact, by the menu system in RiscOS) were selected instead of drop-down menus as being more suitable for a keyboard environment, making better use of available screen space and being easier to deploy on terminals of varied sizes.

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
   
*when_parent_changes_value()*
    Called whenever the parent's *set_value(value)* method is called.
    
*when_value_edited()*
    Called when, during editing of the widget, its value changes.  I.e. after keypresses.
    You can disable this by setting the attribute *check_value_change* to False.
    
    You can override this function for your own use.

*when_cursor_moved()*
    Called when, during the editing of the widget, its cursor has been moved.  You can disable
    the check for this by setting the attribute *check_cursor_move* to False.
    
    You can override this function for your own use. 

Titled Widgets
**************

Many widgets exist in two forms, one with a label, one without.  For example Textbox and TitleText.  If the label is particularly long (at time of construction), the label may be put on its own line.  Additional constructor arguments:

*use_two_lines=*
  If either True or False, override what the widget would otherwise choose. 

*field_width=*
  (For text fields) - how wide should the entry part of the widget be?

*begin_entry_at=16*
   At what column should the entry part of the widget begin?

Internally titled widgets are actually a textbox (for the label) and whatever other kind of widget is required.  You can access the separate widgets (if you ever need to - you shouldn't) through the *label_widget* and *entry_widget* attributes. However, you may never need to, since the *value* and *values* attributes of the combined widget should work as expected.

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
   
   In other words you can pass in a list of objects of arbitrary types. By default, they will be displayed using *str()*, but by overriding *display_value* you can present them however you see fit.
   
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
    
MultiLineAction
    A common use case for this sort of widget is to perform an action on the currently highlighted item when the user pushes Return, Space etc.  Override the method *actionHighlighted(self, act_on_this, key_press)* of this class to provide this sort of widget.  That method will be called when the user 'selects' an item (though in this case .value will not actually be set) and will be passed the item highlighted and the key the user actually pressed.
    
MultiSelectAction
    This is similar to the MultiLineAction widget above, except that it also provides the method *actionSelected(self, act_on_these, keypress)*.  This can be overridden, and will be called if the user pressed ';'.  The method will be passed a list of the objects selected and the keypress.  You probably want to adjust the default keybindings to make this widget useful. 

Dates, Sliders and Combination Widgets
**************************************

DateCombo, TitleDateCombo
    These widgets allow a user to select a date.  The actual selection of a date is done with the class MonthBox, which is displayed in a temporary window.  The constructor can be passed the following arguments - allowPastDate=False and      allowTodaysDate=False - both of which will affect what the user is allowed to select.

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
    

Trees
*****

MultiLineTree, SelectOneTree, and MultiLineTree
    These widgets all work in a very similar way to the non-Tree versions,
    except that they expect to contain an NPSTree in their .values attribute.
    The other major difference is that their .value attribute does not contain
    the index of the selected value(s), but the selected value(s)
    itself/themselves.  However, these classes will in a future version be DEPRECATED in favour of the
    much improved *MultiLineTreeNew* and *MultiLineTreeNewAction* classes. 

MultiLineTreeNew, MultiLineTreeNewAction
    The *values* attribute of this class must store an NPSTree instance.
    However, if you wish you can override the method *convertToTree* of this
    class.  This method should return an NPSTree instance.  The function will be
    called automatically whenever *values* is assigned.

    By default this class uses *TreeLineAnnotated* widgets to display each
    line of the tree.  You can change this by changing the class attribute
    *_contained_widgets*.

Grids
*****
SimpleGrid
    This offers a spreadsheet-like display.  The default is only intended to display information (in a grid of text-fields).  However, it is designed to be flexible and easy to customize to display a variety of different data.  Future versions may include new types of grids.  Note that you can control the look of the grid by specifying either *columns* or *column_width* at the time the widget is created.  It may be that in the future the other multi-line classes will be derived from this class.

    *values* should be specified as a two-dimensional array.

GridColTitles
    Like the simple grid, but uses the first two lines of the display to display the column titles.  These can be provided as a *col_titles* argument at the time of construction, or by setting the *col_titles* attribute at any time.  In either case, provide a list of strings.


Other Controls
**************

Checkbox, RoundCheckBox
   These offer a single option - the label is generated from the attribute *name*, as for titled widgets.  The attribute *value* is either true or false.
   
   The function whenToggled(self) is called when the user toggles the state of the checkbox.  You can overload it.


Button
   Functionally similar to the Checkbox widgets, but looking different.  The Button is usually used for OK and Cancel Buttons on Forms and similar things, though they should probably be replaced with the ButtonPress type.
   
ButtonPress
    Not a toggle, but a control.  This widget has the method whenPressed(self), which you should overload to do your own things.
   
FormControlCheckbox
   A common use of Checkbox is to offer the user the option to enter additional data.  For example "Enter Expiry Date".  In such a case, the Form needs to display additional fields in some cases, but not in others.  FormControlCheckbox makes this trivial.
   
   Two methods are defined:
   
   addVisibleWhenSelected(*wg*)
      *wg* should be a widget.  
      
      This method does not create a widget, but instead puts an existing widget under the control of the FormControlCheckbox.  If FormControlCheckbox is selected, the widget will be visible.  
      
      As many widgets as you wish can be added in this way.
      
   addInvisibleWhenSelected(*wg*)
      Widgets registered in this way are visible only when the FormControlCheckbox is not selected.
      
AnnotateTextboxBase, TreeLineAnnotated
    The AnnotateTextboxBase class is mainly intended for use by the
    multiline listing widgets, for situations where each item displayed needs an
    annotation supplied to the left of the entry itself.  The API for these
    classes is slightly ugly, because these classes were originally intended for
    internal use only.  It is likely that more user-friendly versions will be
    supplied in a later release.  Classes derived from AnnotateTextboxBase
    should define the following:

    *ANNOTATE_WIDTH*
        This class attribute defines how much margin to leave before the
        text entry widget itself.  In the TreeLineAnnotated class the margin needed is calculated
        dynamically, and ANNOTATE_WIDTH is not needed.

    *getAnnotationAndColor* 
        This function should return a tuple consisting of the string to
        display as the annotation and the name of the colour to use when displaying
        it.  The colour will be ignored on B/W displays, but should be provided in
        all cases, and the string should not be longer than *ANNOTATE_WIDTH*,
        although by default the class does not check this.

    *annotationColor*, *annotationNoColor*
        These methods draw the annotation on the screen.  If using strings
        only, these should not need overriding.  If one is altered, the other should
        be too, since npyscreen will use one if the display is configured for colour
        and the other if configured for black and white.

Box Widgets
***********
BoxBasic, RoundCheckBox
   BoxBasic prints a box with an optional name and footer on the screen.  It is intended as a base class 
   for further widgets.
  
BoxTitle
    BoxTitle is a hybrid of the Title widget and the Multiline widget.  Again, it is mostly intended as a base
    class for more complex layouts.



All about Key Bindings
======================

What is going on
****************

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
         "^P":              self.h_exit_up,
         "^N":              self.h_exit_down,
         curses.ascii.ESC:  self.h_exit_escape,
         curses.KEY_MOUSE:  self.h_exit_mouse,
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

All of the standard widgets are entirely usable on a monochrome terminal.  However, it's a colourful world these days, and npyscreen lets you display your widgets in, well, if not Technicolor(TM) then as close as curses will allow.

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

Enhancing Mouse Support
***********************
Widgets that wish to handle mouse events in more detail should override the method *.handle_mouse_event(self, mouse_event)*.  Note that *mouse_event* is a tuple::
    
    def handle_mouse_event(self, mouse_event):
        mouse_id, x, y, z, bstate = mouse_event
        # Do things here....

x and y are the mouse click's position on the screen.  Presumably the widget would need to also do::
    
    x = x-self.relx
    y = y-self.rely

See the Python Library curses module documentation for more detail on mouse events.

How Widgets use colour
**********************

When a widget is being drawn, it asks the active ThemeManager to tell it appropriate colours.  'LABEL', for example, is a label given to colours that will be used for the labels of widgets.  The Theme manager looks up the relevant name in its *default_colors* dictionary and returns the appropriate colour-pair as an curses attribute that is then used to draw the widget on the screen.

Individual widgets often have *color* attribute of their own (which may be set by the constructor).  This is usually set to 'DEFAULT', but could be changed to any other defined name.  This mechanism typically only allows individual widgets to have one particular part of their colour-scheme changed.

Title... versions of widgets also define the attribute *labelColor*, which can be used to change the colour of their label colour.

Unicode
*******
The latest versions of the library aim to handle unicode/utf-8 strings.  Please report any problems.

