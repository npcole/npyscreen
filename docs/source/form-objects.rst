Form Objects
============

A Form object is a screen area that contains widgets.  Forms control which widget a user is editing, and may provide additional functionality, such as pop-up menus or actions that happen on particular keypresses.

Creating a Form
***************

.. py:class:: Form(name=None, lines=0, columns=0, minimum_lines=24, minimum_columns=80)

Forms have the following class attributes::

    DEFAULT_LINES      = 0
    DEFAULT_COLUMNS    = 0
    SHOW_ATX           = 0
    SHOW_ATY           = 0

The default values will create a form that fills the whole screen and which is displayed in the top left corner.  See the arguments passed in to the constructor for more details on controlling the size of a form.  

The Following arguments can be passed to a Form's constructor:

*name=*
    Names the Form.  As for some widgets, this will display a title.

*lines=0, columns=0, minimum_lines=24, minimum_columns=80*
    You can adjust the size of the Form, either providing an absolute size (with *lines=* and *columns=*) or a minimum size (*minimum_lines=* and *minimum_columns=*).  The default minimums (24x80) provide the standard size for terminal.  If you plan your Forms to fit within that size, they should be viewable on almost all systems without the need to scroll the Form.  Note that you can use the absolute sizing in one direction and the minimum in the other, should you wish.
    
The standard constructor will call the method *.create()*, which you should override to create the Form widgets.  See below.

Placing widgets on a Form
*************************

To add a widget to a Form, use the method:

.. py:method:: Form.add(WidgetClass, ...)

    WidgetClass must be a class, all of the additional arguments will be passed to the widget's own constructor.  A     reference to the widget will be returned.


The position and size of a widget are controlled by the widget's constructor.  However, there are hints that the Form class provides.  If you do not override the position of the widget, it will be placed according to the Form's *.nextrelx* and *nextrely* instance attributes.  The *.nextrely* attribute is increased automatically each time a widget is placed.  You might also increase it yourself by doing something like::
   
   self.nextrely += 1

Which would leave a gap between the previous widget and the next placed one.

.. py:attribute:: Form.nextrely
    
    The y position at which the next created widget should be made.  The standard forms set this to the line below the previously created widget as each widget is added to the form.

.. py:attribute:: nextrelx
    
    The x position at which the next created widget should be made.
    
    
Other Standard Form Features
****************************

.. py:method:: Form.create
    
    This method is called by the Form's constructor.  It does nothing by default - it is there for you to override in
    subclasses, but it is the best place to set up all the widgets on a Form.  Expect this method to be full of
    *self.add(...)* method calls, then!


.. py:method:: Form.while_editing

    This method is called as the user moves between widgets.  It is intended for you to override in subclasses, to do things like altering one widget based on the value of another.


.. py:method:: Form.adjust_widgets

    Be very careful with this method.  It is called for every keypress while the Form is being edited, and there is no guarantee that it might not be called even more frequently.  By default it does nothing, and is intended for you to override.  Since it gets called so frequently, thoughtlessness here could slow down your whole application.  
    
    For example, be very conservative with redraws of the whole Form (a slow operation) - make sure you put in code to test whether a redraw is necessary, and try to only redraw widgets that really need to be changed, rather than redrawing the whole screen.
   
    If the Form's parentApp also has a method called *adjust_widgets*, this will also be called.

 
.. py:method:: Form.while_waiting

   If you wish to perform actions while waiting for the user to press a key, you may define a *while_waiting* method.  You should also set the attribute *keypress_timeout*, which is a value in ms.  Whenever waiting for input, if more than the time given in *keypress_timeout* passes, while_waiting will be called.  Note that npyscreen takes no steps to ensure that *while_waiting()* is called at exactly regular intervals, and in fact it may never be called at all if the user continually presses keys.
   
   If a form's parentApp has a method called *while_waiting* this will also be called.
   
   A *keypress_timeout* value of 10 suggests that the *while_waiting* method is called about every second, assuming the user takes no other action.
   
   See the included example Example-waiting.py for a fully worked example.

.. py:attribute:: Form.keypress_timeout
    
    See the `while_waiting` method above. 
   
   
.. py:method:: Form.set_value(value)

    Store *value* in the *.value* attribute of the *Form* and then call the *whenParentChangeValue* method of every widget that has it.  
    
    
.. py:attribute: Form.value

    All form classes can have the method *set_value(value)*.  This sets the value of the attribute *value* and calls the method *when_parent_changes_value* of every contained widget on the form.

    

Displaying and Editing Forms
****************************

.. py:method:: Form.display()

    Redraw every widget on the Form and the Form itself.

.. py:method:: Form.DISPLAY()

    Redraw the form, but make extra sure that the display is reset.  This is a slow operation, and avoid calling if possible.  You may sometimes need to use this if an external process has disrupted the terminal.

.. py:method:: Form.edit()

    Allow the user to interactively edit the value of each widget.  You should not need to call this method if correctly using the *NPSAppManaged* class.  You should avoid calling this method if possible, but you will need to use it if writing simple applications that do not use the NPSAppManaged class.  Calling this method directly is akin to creating a modal dialog box in a GUI application.  As far as possible consider this method an internal API call.

When forms exit
~~~~~~~~~~~~~~~

    Forms may exit their editing modes for a number of reasons.  In NPSAppManaged applications, the controlling application may cause the form to exit.
    
    Setting the attribute `.editing` to False yourself, however, will cause the form to exit.


Standard Form Classes
*********************

.. py:class:: Form

   The basic Form class.  When editing the form, the user can exit by selecting the OK button in the bottom right corner.
   
   By default, a Form will fill the Terminal.  Popup is simply a Form with a smaller default size.


.. py:class:: Popup
   
   Popup is simply a Form with a smaller default size.
   
   
.. py:class:: ActionForm

   The ActionForm creates OK and Cancel buttons.  Selecting either exits the form.  The method *on_ok* or *on_cancel* is called when the Form exits (assuming the user selected one of these buttons).  Subclasses may therefore usefully override one or both of these methods, which by default do nothing.
   
    .. py:method:: on_ok
    
        Called when the ok button is pressed.  Setting the attribute `.editing` to True in this method will abort editing the form.
    
    .. py:method:: on_cancel
    
        Called when the cancel button is pressed. Setting the attribute `.editing` to True in this method will abort editing the form.

.. py:class:: ActionFormV2

   New in Version 4.3.0.  This version of ActionForm behaves similarly to ActionForm above, but the code is much cleaner.  It should 
   be much easier to subclass.  Eventually, this version may entirely replace ActionForm.

.. py:class:: ActionFormMinimal

    New in Version 4.4.0.  This version of ActionFormV2 only features an OK button.  Added at user request for use in
    special circumstances.  

.. py:class:: ActionPopup
    
    A smaller version of the ActionForm.
   
   
.. py:class::TitleForm

    A more minimal form with just a title bar, rather than a full border.

.. py:class::TitleFooterForm
    
    A minimal form with a title bar and a bar along the bottom.

.. py:class:: SplitForm
   
   The SplitForm has a horizontal line across the middle.  The method *get_half_way()* will tell you where it has been drawn.
   
    .. py:attribute:: draw_line_at
       
       This attribute defines the position at which the line should be drawn across the screen.  It can be set by passing `draw_line_at=`
       to the constructor, or will be set automatically at the value returned by the method `get_half_way`.
   
    .. py:method:: get_half_way

        return the y co-ordinate of the bar across the middle of the form.  In fact in subclasses of this form, there is no
        particular reason why the y co-ordinate should in fact be half way down the form, and subclasses may return whatever
        value is convenient.
    
    .. py:attribute:: MOVE_LINE_ON_RESIZE
        
        This class attribute specifies whether the position of the line should be moved when the form is resized.  Since 
        any widgets below the line would also need to be moved (presumably in an overriden `resize` method on subclasses of
        this form, this value is set to False by default).

   
.. py:class:: FormWithMenus
    
    Similar to the Form class, but provides the additional functionality of Popup menus.
   
    To add a new menu to the Form use the method *new_menu(name='')*.  This will create the menu and return a proxy to it.  For more details see the section on Menus below.


.. py:class:: ActionFormWithMenus

   Similar to the ActionForm class, but provides the additional functionality of Popup menus.
   
   To add a new menu to the Form use the method *new_menu(name='')*.  This will create the menu and return a proxy to it.  For more details see the section on Menus below.
   
.. py:class:: ActionFormV2WithMenus

   New in Version 4.3.0.  This version of ActionFormWithMenus behaves similarly to ActionForm above, but the code is much cleaner.  It should 
   be much easier to subclass.  Eventually, this version may entirely replace ActionFormWithMenus.
   
   
.. py:class:: FormBaseNew

    This form does not have an *ok* or *cancel* button by default.  The additional methods *pre_edit_loop* and *post_edit_loop* are called before and after the Form is edited.  The default versions do nothing.  This class is intended as a base for more complex user interfaces.
    
    .. py:method:: pre_edit_loop

        Called before the form is edited.

    .. py:method:: post_edit_loop

        Called after the edit loop exits.

.. py:class:: FormBaseNewWithMenus
    
    Menu-enabled version of FormBaseNew.


Mutt-like Forms
***************

    
.. py:class:: FormMutt

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
    
FormMuttActive, FormMuttActiveWithMenus, FormMuttActiveTraditional, FormMuttActiveTraditionalWithMenus
    These classes are intended to make the creation of more complicated applications easier.  Each class uses the additional classes *NPSFilteredDataBase*, *ActionControllerSimple*, *TextCommandBox*, *TextCommandBoxTraditional*.
    
    A very common \*nix style of terminal application (used by applications like mutt and irssi) has a central display with a list or grid of times, a command line at the bottom and some status lines.
    
    These classes make setting up a similar form easy.  The difference between the *FormMuttActive* and *FormMuttActiveTraditional* classes is that in the latter the only widget that the user ever actually edits is the command line at the bottom of the screen.  However, keypresses will be passed to the multiline widget in the centre of the display if these widgets are not editing a command line, allowing the user to scroll around and select items.
    
    What is actually displayed on the screen is controlled by the *ActionControllerSimple* class, which uses as a base the data stored not by any of the individual widgets but by the *NPSFilteredDatabase* class.
    
    See the section on writing Mutt-like applications later in this documentation for more information.
    
    
Multi-page Forms
****************

.. py:class:: FormMultiPage (new in version 2.0pre63)

    This *experimental* class adds support for multi-page forms.  By default, scrolling down off the last widget on a page moves to the next page, and moving up from the first widget moves back a page. 
    
    The default class will display the page you are on in the bottom right corner if the attribute *display_pages* is True and if there is more than one page.  You can also pass *display_pages=False* in to the constructor.  The color used for this display is stored in the attribute *pages_label_color*.  By default this is 'NORMAL'.  Other good values might be 'STANDOUT', 'CONTROL' or 'LABEL'. Again, you can pass this in to the constructor.
        
    Please note that this class is EXPERIMENTAL.  The API is still under review, and may change in future releases.  It is intended for applications which may have to create forms dynamically, which might need to create a single form larger than a screen (for example, a Jabber client that needs to display an xmpp form specified by the server.)  It is *not* intended to display arbitrarily large lists of items.  For that purpose, the multiline classes of widgets are much more efficient.
    
    
    Three new methods are added to this form:
    
.. py:method:: FormMultiPage.add_page()

        Intended for use during the creation of the form.  This adds a new page, and resets the position at which new widgets will be added.  The index of the page added is returned.
        
.. py:method:: FormMultiPage.switch_page(*index*) 

        This method changes the active page to the one specified by *index*.
    
.. py:method:: FormMultiPage.add_widget_intelligent(*args, **keywords)

        This method adds a widget to the form.  If there is not enough space on the current page, it tries creating a new page and adding the widget there.  Note that this method may still raise an exception if the user has specified options that prevent the widget from appearing even on the new page.
        
        
.. py:class:: FormMultPageAction (new in version 2.0pre64)

    This is an *experimental* version of the FormMultiPage class that adds the on_ok and on_cancel methods of the ActionForm class and automatically creates cancel and ok buttons on the last page of the form.
    
.. py:class:: FormMultiPageWithMenus

    Menu-enabled version of MultiPage.

.. py:class:: FormMultiPageActionWithMenus

    Menu-enabled version of MultiPageAction.


Menus
*****

Some Form classes support the use of popup menus.  Menus could in theory be used as widgets on their own.  Popup menus (inspired, in fact, by the menu system in RiscOS) were selected instead of drop-down menus as being more suitable for a keyboard environment, making better use of available screen space and being easier to deploy on terminals of varied sizes.

By default, the supporting forms will display an advert that the menu system is available to the user, and a shortcut to the list of menus.  If the form has multiple menus, a 'root' menu listing all of them will be displayed.

Menus are usually created by calling a (supporting) Form's *new_menu* method.  Version 2.0pre82 adds the argument *shortcut=None* to this method.  In the list of menus that the Form displays, this shortcut will be displayed.  After a menu has been created, the following methods on that object are useful:

.. py:method:: NewMenu.addItem(text='', onSelect=function, shortcut=None, arguments=None, keywords=None)

   *text* should be the string to be displayed on the menu.  `onSelect` should be a function to be called if that item is selected by the user.  This is one of the few easy opportunities in npyscreen to create circular references - you may wish to pass in a proxy to a function instead.  I've tried to guard you against circular references as much as possible - but this is just one of those times I can't second-guess your application structure. Version 2.0pre82 adds the ability to add a shortcut. 
   
   From version 3.6 onwards, menu items can be specified with a list of *arguments* and/or a dictionary of keywords.
   
.. py:method:: NewMenu.addItemsFromList(item_list)

	The agument for this function should be a list or tuple. Each element of this should be a tuple of the arguments that are used for creating each item.  This method is DEPRECATED and may be removed or altered in a future version.
   
.. py:method:: NewMenu.addNewSubmenu(name=None, shortcut=None, preDisplayFunction=None, pdfuncArguments=None, pdfuncKeywords=None)

   Create a new submenu (returning a proxy to it).  This is the preferred way of creating submenus. Version 2.0pre82 adds the ability to add a keyboard shortcut.
   
   From version 3.7 onwards, you can define a function and arguments to be called before this menu is displayed.  This might mean you
   can adjust the content of the menu at the point it is displayed.  Added at user request.
   
.. py:method:: NewMenu.addSubmenu(submenu)

    Add an existing Menu to the Menu as a submenu.  All things considered, addNewSubmenu is usually a better bet.

    
(Internally, this menu system is referred to as the "New" menu system - it replaces a drop-down menu system with which I was never very happy.)


Resizing Forms (New in version 2.0pre88)
****************************************

When a form is resized, a signal is sent to the form currently on the screen.  Whether or not the form handles this is decided by three things.

If you set the variable `npyscreen.DISABLE_RESIZE_SYSTEM` to True, forms will not resize at all.

The class attribute `ALLOW_RESIZE` (=True by default).
	If this is set to false the form will not resize itself.
	
The class attribute `FIX_MINIMUM_SIZE_WHEN_CREATED` controls whether the form can be made smaller than the size it was when it was created.  By default this is set to `False`.  This is because for over a decade, npyscreen assumed that forms would never change size, and many programs may rely on the fact that the form will never be resized.  If you are writing new code from scratch, you can set this value to True, provided that you test the results to make sure that resizing the form will not crash your application.

When a form is resized, the method `resize` will be called *after* the new size of the form has been fixed.  Forms may override this method to move widgets to new locations or alter anything else about the layout of the form as appropriate.

When using the `NPSAppManaged` system, forms will be automatically resized before they are displayed.

