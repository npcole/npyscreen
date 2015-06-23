Widgets: Basic Features
=======================

Creating Widgets
****************

Widgets are created by passing their class as the first argument of a Form's *add(...)* method.  The remaining arguments will be passed to the widget's own constructor.  These control things such as size, position, name, and initial values.

Constructor arguments
*********************

*name=*
  You should probably give each widget a name (a string).  Where appropriate, it will be used as the label of the widget.

*relx=*, *rely=*
   The position of the widget on the Form is controlled by relx and rely integers.   You don't have to specify them, in which case the form will do its best to decide where to put the widget.  You can specify only one or the other if you so choose (eg. you probably don't usually need to specify relx).  *New in Version 4.3.0*: if you give a negative value for rely or relx, the widget will be positioned relative to the bottom or right hand side of the Form.  If the form is resized, npyscreen will do its best to keep the widget in place.

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

*update(clear=True)*
   Redraws the widget, but doesn't tell curses to update the screen (it is more efficient to update all widgets and then have the Form on which they sit tell curses to redraw the screen all in one go).

   Most widgets accept the optional argument *clear=False|True* which affects whether they first blank the area they occupy before redrawing themselves.
   
*when_parent_changes_value()*
    Called whenever the parent form's *set_value(value)* method is called.
    
*when_value_edited()*
    Called when, during editing of the widget, its value changes.  I.e. after keypresses.
    You can disable this by setting the attribute *check_value_change* to False.
    
    You can override this function for your own use.

*when_cursor_moved()*
    Called when, during the editing of the widget, its cursor has been moved.  You can disable
    the check for this by setting the attribute *check_cursor_move* to False.
    
    You can override this function for your own use. 

*edit()*
   Allow the user to interact with the widget.  The method returns when the user leaves the widget.  In most cases, you will never need to call this method yourself, and for the most part this should be regarded as part of the internal API of npyscreen.

*set_relyx()*
    Set the position of the widget on the Form.  If y or x is a negative value,
    npyscreen will try to position it relative to the bottom or right edge of the 
    Form.  Note that this ignores any margins that the Form may have defined. 
    (New in Version 4.3.0).
    

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

Creating your own widgets
*************************

All widgets should inherit from the class `Widget`.  

*calculate_area_neeeded*
    This function is called to ask the widget how many lines and columns it requires (for a minimal display).  You should return a tuple with exactly two numbers.  Returning 0 for either argument says that the widget should be given all the remaining space on the display if it is available.
    
If you are writing text to the screen you should avoid using curses directly, and instead use the function

*add_line(realy, realx, unicode_string, attributes_list, max_columns, force_ascii=False)*
    This function adds a line of text to the display. `realy` and `realx` are the absolute position on the Form. `attributes_list` is a list of attributes that should be applied to each character.  If all of them require the same attribute, use the `make_attributes_list` method to create a list of the right length.
    
*make_attributes_list(unicode_string, attribute)*
    A convenience function.  Retuns a list the length of the unicode_string provided, with each entry of the list containing a copy of attribute.

*resize()*
    You can override this method to perform any necessary actions when the widget is resized.  (New in version 4.3.0)