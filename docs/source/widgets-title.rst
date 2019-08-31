Widgets: Titled Widgets
***********************

Most versions of the standard widget set come in two forms - a basic version and a corresponding version that also prints a label with the name of the widget.  For example, Textfield and TitleText.

The Title versions are in fact a wrapper around a contained widget, rather than being a proper widget in their own right, and this can be a cause of confusion when modifying their behaviour.  

In general, to create your own version of these widgets, you should first create the contained widget, and then create a titled version.

For example::

	class NewTextWidget(textbox.Textfield):
		# all of the custom code for this class
		# should go here.
		
	
	class TitleProductSearch(TitleText):
		_entry_type = NewTextWidget

You can adjust where the child widget is placed on the screen by passing in the argument *begin_entry_at* to the constructor. The default is 16. You can also override whether the widget uses a separate line for the title by passing in the argument *use_two_lines=True|False* at the time the widget is created.  The default *use_two_lines=None* will keep the title and the contained widget on the same line, unless the label is too long.

You can change the label color at creation time using the argument *labelColor='LABEL'*.  You can specify any of the color names from the theme you are using.

After creation, the two widgets managed by the TitleWidget can be accessed through the *label_widget* and *entry_widget* attributes of the object. 
		

Titled multiline widgets
++++++++++++++++++++++++

If you are creating titled versions of the multiline widgets, you will find it better to inherit from the class `TitleMultiLine` instead, which wraps more of the multiline functionality.


Widgets: Box Widgets
********************

These widgets work in a similar way to the Titled versions of widgets.  The box widget contains a widget of another class.  


BoxBasic
   BoxBasic prints a box with an optional name and footer on the screen.  It is intended as a base class for further widgets, not for direct use.
  
BoxTitle
    BoxTitle is a hybrid of the Title widget and the Multiline widget.  Again, it is mostly intended as a base class for more complex layouts.  This class has a `_contained_widget` attribute that puts a widget inside the box when the class is created.  In the Boxtitle class this is a Multiline widget.  The title of the widget can be passed to `__init__` the parameter `name=....`.  Another perimeter  `footer=...` gives the text for the footer of the box.  These correspond to attributes named `name` and `footer` which can be changed at any time. 
    
    The attribute `entry_widget` gives direct access to the contained widget.
    
    The properties `editable`, `values`, and `value` give direct access to the attributes of `entry_widget`.
	
	The constructor for this widget can be passed the argument `contained_widget_arguments`. This should be a dictionary of arguments that will be passed to the entry_widget when it is created.  Note that no sanity checking is done on this dictionary at this time. (New in version 4.8.0)
	
Your own versions of these widgets can be created in the same way as new Titled widgets.  Create the contained widget class first, and then create the box class wrapper class::

	class NewMultiLineClass
		# Do all sorts of clever things here!
		# ....

	 class BoxTitle(BoxBasic):
	     _contained_widget = NewMultiLineClass
		 
	 
