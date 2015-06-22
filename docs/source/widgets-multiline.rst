Widgets: Picking Options
************************

MultiLine
   Offer the user a list of options.  (This widget could probably have a better name, but we're stuck with it for now)

   The options should be stored in the attribute *values* as a list.  The attribute *value* stores the index of the user's selection.  If you want to return the actual selected values rather than an index, use the *get_selected_objects()* method.

   One of the most important features of MultiLine and widgets derived from it is that it can be adapted easily to allow the user to choose different types of objects.  To do so, override the method *display_value(self, vl)*.  The argument *vl* will be the object being displayed, and the function should return a string that can be displayed on the screen.
   
   In other words you can pass in a list of objects of arbitrary types. By default, they will be displayed using *str()*, but by overriding *display_value* you can present them however you see fit.
   
   MultiLine also allows the user to 'filter' entries.  (bound to keys l, L, n, p by default for filter, clear filter, next and previous). The current implementation highlights lines that match on the screen.  Future implementations may hide the other lines or offer a choice.  You can control how the filter operates by overriding the filter_value method.  This should accept an index as an argument (which looks up a line in the list .values) and should return True on a match and False otherwise.  From version 2.0pre74, the whole filtering system can be disabled by setting that attribute *.allow_filtering* to False.  This can also be passed in as an argument to the constructor.
    
    Multiline widgets are a container widget that then holds a series of other widgets that handle various parts of the display.  All multiline classes have a `_contained_widget` class attribute. This controls how the widget is constructed.  The class attribute `_contained_widget_height` specifies how many lines of the screen each widget should be given.


TitleMultiLine
   A titled version of the MultiLine widget.  

   If creating your own subclasses of MultiLine, you can create Title versions by subclassing this object and changing the *_entry_type* class variable.

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
    
BufferPager, TitleBufferPager *New in Version 2.0pre90*
    The `BufferPager` class is a subclass of the *Pager* class.  It is designed to display text to the user in much the way that `tail -f` does under *nix.  By default, the .values attribute is set to an instance of the `collections.deque` class.  You can pass a `maxlen=` value to the constructor.  If not, the maxlen for the deque object will be taken from the class attribute `DEFAULT_MAXLEN`, which is None by default.
    
    .. py:method:: BufferPager.clearBuffer()
    
        Clear the buffer.
        
    .. py:method:: BufferPager.buffer(lines, scroll_end=True, scroll_if_editing=False)
    
        Add `lines` to the contained deque object.  If `scroll_end` is True, scroll to the end of the buffer.  If `scroll_if_editing` is True, then scroll to the end even if the user is currently editing the Pager.  If the contained deque object was created with a maximum length, then new data may cause older data to be forgotten.
        
MultiLineEditable
    A list of items that the user can edit, based on the multiline classes.  New in version 3.9
    
    .. py:method:: get_new_value()
        
        This method should return a 'blank' object that can be used to initialize a new item on the list.  By default it returns an
        empty string.
        

    .. py:mehod:: check_line_value(vl)
        
        This method should say whether vl is a valid object that can be added to the list, returning True or False.  By default, this 
        method rejects empty strings.
    
MultiLineEditableTitle
    A titled version of MultiLineEditable. The class attribute *_entry_type* controls the type of contained widget.
    
MultiLineEditableBoxed
    A boxed version of MultiLineEditable. The class attribute **_entry_type* controls the type of contained widget.

        
Custom Multiselect Widgets
++++++++++++++++++++++++++

Multiline widgets are a container widget that then holds a series of other widgets that handle various parts of the display.  All multiline classes have a `_contained_widget` class attribute. This controls how the widget is constructed.  The class attribute `_contained_widget_height` specifies how many lines of the screen each widget should be given.

From version 3.4 onwards, contained widgets that have a `.selected` attribute are handled differently: widgets will have their `.selected` attribute set to `True` if the line is selected and `False` otherwise.  Widgets may also have their `.important` attribute set to True or False, depending on if they are included in a current filter (see above).

Widgets that do not have a `selected` attribute have the value for each line put in their `name` attribute, and whether the line is selected or not put in their `value` attribute.  This is a legacy of the fact that the standard multiselect widgets use checkboxes to display each line.

From version 4.8.7 onwards, multiline widgets use the methods `set_is_line_important`, `set_is_line_bold` and `set_is_line_cursor` to control the display of each line.  These methods are passed the widget object in question and a Boolean value.  They are intended to be overridden. 

