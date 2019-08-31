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
        'FORMDEFAULT' : 'WHITE_BLACK',
        'NO_EDIT'     : 'BLUE_BLACK',
        'STANDOUT'    : 'CYAN_BLACK',
        'CURSOR'      : 'WHITE_BLACK',
        'CURSOR_INVERSE': 'BLACK_WHITE',
        'LABEL'       : 'GREEN_BLACK',
        'LABELBOLD'   : 'WHITE_BLACK',
        'CONTROL'     : 'YELLOW_BLACK',
        'IMPORTANT'   : 'GREEN_BLACK',
        'SAFE'        : 'GREEN_BLACK',
        'WARNING'     : 'YELLOW_BLACK',
        'DANGER'      : 'RED_BLACK',
        'CRITICAL'    : 'BLACK_RED',
        'GOOD'        : 'GREEN_BLACK',
        'GOODHL'      : 'GREEN_BLACK',
        'VERYGOOD'    : 'BLACK_GREEN',
        'CAUTION'     : 'YELLOW_BLACK',
        'CAUTIONHL'   : 'BLACK_YELLOW',
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


Defining custom colours (strongly discouraged)
***********************************************

On some terminals, it is possible to define custom colour values.  rxvt/urxvt is one such terminal.  From version 4.8.4 onwards, support for this is built in
to theme manager classes.  

The class variable color_values will be used when the class is initialized to redefine custom colour values::

	_color_values = (
			# redefining a standard color
	        (curses.COLOR_GREEN, (150,250,100)),
			# defining another color
			(70, (150,250,100)),
	    )
		
NB. Current versions of npyscreen make no effort to reset these values when the application exits.

Use of this facility is discouraged, because it is impossible to tell reliably whether or not a terminal actually supports custom colours.  This feature was added at user request to support a custom application.
