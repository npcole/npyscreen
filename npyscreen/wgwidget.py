#!/usr/bin/python

import sys
import curses
import curses.ascii
import curses.wrapper
import weakref
from . import npysGlobalOptions as GlobalOptions
import locale
import warnings


EXITED_DOWN  =  1
EXITED_UP    = -1
EXITED_LEFT  = -2
EXITED_RIGHT =  2
EXITED_ESCAPE= 127
EXITED_MOUSE = 130

SETMAX       = 'SETMAX'
RAISEERROR   = 'RAISEERROR'

class InputHandler(object):
    "An object that can handle user input"

    def handle_input(self, _input):
        """Returns True if input has been dealt with, and no further action needs taking.
        First attempts to look up a method in self.input_handers (which is a dictionary), then
        runs the methods in self.complex_handlers (if any), which is an array of form (test_func, dispatch_func).
        If test_func(input) returns true, then dispatch_func(input) is called. Check to see if parent can handle.
        No further action taken after that point."""
        
        if _input in self.handlers:
            self.handlers[_input](_input)
            return True

        elif curses.ascii.unctrl(_input) in self.handlers:
            self.handlers[curses.ascii.unctrl(_input)](_input)
            return True


        else:
            if not hasattr(self, 'complex_handlers'): return False
            for test, handler in self.complex_handlers:
                if test(_input): 
                    handler(_input)
                    return True
        if hasattr(self, 'parent') and hasattr(self.parent, 'handle_input'):
            if self.parent.handle_input(_input):
                return True

        else:
            pass

    # If we've got here, all else has failed, so:
        return False

    def set_up_handlers(self):
        """This function should be called somewhere during object initialisation (which all library-defined widgets do). You might like to override this in your own definition,
but in most cases the add_handers or add_complex_handlers methods are what you want."""
        #called in __init__
        self.handlers = {curses.ascii.NL:  self.h_exit_down,
                           curses.ascii.CR:  self.h_exit_down,
                   curses.ascii.TAB: self.h_exit_down,
                   curses.KEY_DOWN:  self.h_exit_down,
                   curses.KEY_UP:    self.h_exit_up,
                   curses.KEY_LEFT:  self.h_exit_left,
                   curses.KEY_RIGHT: self.h_exit_right,
                   "^P":                self.h_exit_up,
                   "^N":                self.h_exit_down,
                   curses.ascii.ESC:    self.h_exit_escape,
                   curses.KEY_MOUSE:    self.h_exit_mouse,
                   }

        self.complex_handlers = []

    def add_handlers(self, handler_dictionary):
        """Update the dictionary of simple handlers.  Pass in a dictionary with keyname (eg "^P" or curses.KEY_DOWN) as the key, and the function that key should call as the values """
        self.handlers.update(handler_dictionary)
    
    def add_complex_handlers(self, handlers_list):
        """add complex handlers: format of the list is pairs of
        (test_function, callback) sets"""

        for pair in handlers_list:
            assert len(pair) == 2
        self.complex_handlers.extend(handlers_list)

###########################################################################################
# Handler Methods here - npc convention - prefix with h_

    def h_exit_down(self, _input):
        """Called when user leaves the widget to the next widget"""
        self.editing = False
        self.how_exited = EXITED_DOWN
        
    def h_exit_right(self, _input):
        self.editing = False
        self.how_exited = EXITED_RIGHT

    def h_exit_up(self, _input):
        """Called when the user leaves the widget to the previous widget"""
        self.editing = False
        self.how_exited = EXITED_UP
        
    def h_exit_left(self, _input):
        self.editing = False
        self.how_exited = EXITED_LEFT
        
    def h_exit_escape(self, _input):
        self.editing = False
        self.how_exited = EXITED_ESCAPE

    def h_exit_mouse(self, _input):
        self.editing = False
        self.how_exited = MOUSE_EVENT
    



class Widget(InputHandler):
    "A base class for widgets. Do not use directly"

    def destroy(self):
        """Destroy the widget: methods should provide a mechanism to destroy any references that might
        case a memory leak.  See select. module for an example"""
        pass

    def __init__(self, screen, 
            relx=0, rely=0, name=None, value=None, 
            width = False, height = False,
            max_height = False, max_width=False,
            editable=True,
            hidden=False,
            color='DEFAULT',
            use_max_space=False,
            **keywords):
        """The following named arguments may be supplied:
        name= set the name of the widget.
        width= set the width of the widget.
        height= set the height.
        max_height= let the widget choose a height up to this maximum.
        max_width=  let the widget choose a width up to this maximum.
        editable=True/False the user may change the value of the widget.
        hidden=True/False The widget is hidden.
        """
        
        self.hidden = hidden
        try:
            self.parent = weakref.proxy(screen)
        except TypeError:
            self.parent = screen
        self.relx = relx
        self.rely = rely
        self.use_max_space = use_max_space
        self.color = color
        
        self.set_up_handlers()
        
        # To allow derived classes to set this and then call this method safely...
        try:
            self.value
        except AttributeError:
            self.value = value

        # same again
        try:
            self.name
        except:
            self.name=name
            
        self.request_width =  width     # widgets should honour if possible
        self.request_height = height    # widgets should honour if possible

        self.max_height = max_height
        self.max_width = max_width

        self.set_size()

        self.editing = False        # Change to true during an edit
        
        self.editable = editable
        if self.parent.curses_pad.getmaxyx()[0]-1 == self.rely: self.on_last_line = True
        else: self.on_last_line = False
        
        
    def do_colors(self):
        "Returns True if the widget should try to paint in coloour."
        if curses.has_colors() and not GlobalOptions.DISABLE_ALL_COLORS:
            return True
        else:
            return False
        
    def space_available(self):
        """The space available left on the screen, returned as rows, columns"""
        if self.use_max_space:
            y, x = self.parent.useable_space(self.rely, self.relx)
        else:
            y, x = self.parent.widget_useable_space(self.rely, self.relx)
        return y,x

    def calculate_area_needed(self): 
        """Classes should provide a function to
calculate the screen area they need, returning either y,x, or 0,0 if
they want all the screen they can.  However, do not use this to say how
big a given widget is ... use .height and .width instead"""
        return 0,0

    def set_size(self):
        """Set the size of the object, reconciling the user's request with the space available"""
        my, mx = self.space_available()
        #my = my+1 # Probably want to remove this.
        ny, nx = self.calculate_area_needed()
        
        max_height = self.max_height
        max_width  = self.max_width
        if max_height not in (None, False) and max_height < 0:
            max_height = my + max_height
        if max_width not in (None, False) and max_width < 0:
            max_width = mx + max_width
        if max_height not in (None, False) and max_height <= 0:
            raise Exception("Not enough space for requested size")  
        if max_width not in (None, False) and max_width <= 0:
            raise Exception("Not enough space for requested size")
        
        if ny > 0:
            if my >= ny: self.height = ny
            else: self.height = RAISEERROR
        elif max_height:
            if max_height < my: self.height = max_height
            else: 
                self.height = self.request_height
        else: self.height = (self.request_height or my)
        
        #if mx <= 0 or my <= 0:
        #    raise Exception("Not enough space for widget")


        if nx > 0:                 # if a minimum space is specified....
            if mx >= nx:           # if max width is greater than needed space 
                self.width = nx    # width is needed space
            else: 
                self.width = RAISEERROR    # else raise an error
        elif self.max_width:       # otherwise if a max width is speciied
            if max_width <= mx: 
                self.width = max_width
            else: 
                self.width = RAISEERROR
        else: 
            self.width = self.request_width or mx

        if self.height == RAISEERROR or self.width == RAISEERROR:
            # Not enough space for widget
            raise Exception("Not enough space: max y and x = %s , %s. Height and Width = %s , %s " % (my, mx, self.height, self.width) ) # unsafe. Need to add error here.
    def update(self):
        """How should object display itself on the screen. Define here, but do not actually refresh the curses
        display, since this should be done as little as possible.  This base widget puts nothing on screen."""
        if self.hidden:
            self.clear()
            return True

    def display(self):
        """Do an update of the object AND refresh the screen"""
        self.update()
        self.parent.refresh()

    def set_editable(self, value):
        if value: self._is_editable = True
        else: self._is_editable = False

    def get_editable(self):
        return(self._is_editable)

    def clear(self, usechar=' '):
        """Blank the screen area used by this widget, ready for redrawing"""
        for y in range(self.height):
#This method is too slow
#           for x in range(self.width+1):
#               try:
#                   # We are in a try loop in case the cursor is moved off the bottom right corner of the screen
#                   self.parent.curses_pad.addch(self.rely+y, self.relx + x, usechar)
#               except: pass
#Use this instead
            self.parent.curses_pad.addstr(self.rely+y, self.relx, usechar * (self.width))  # used to be width + 1

    def edit(self):
        """Allow the user to edit the widget: ie. start handling keypresses."""
        self.editing = 1
        self._pre_edit()
        self._edit_loop()
        return self._post_edit()

    def _pre_edit(self):
        self.highlight = 1
        old_value = self.value
        self.how_exited = False

    def _edit_loop(self):
        while self.editing:
            self.display()
            self.get_and_use_key_press()

    def _post_edit(self):
        self.highlight = 0
        self.update()
        


    def try_adjust_widgets(self):
        if hasattr(self.parent, "adjust_widgets"):
            self.parent.adjust_widgets()
    
    def try_while_waiting(self):
        if hasattr(self.parent, "while_waiting"):
            self.parent.while_waiting()

    def get_and_use_key_press(self):
            curses.meta(1)
            self.parent.curses_pad.keypad(1)
            if self.parent.keypress_timeout:
                curses.halfdelay(self.parent.keypress_timeout)
                ch = self.parent.curses_pad.getch()
                if ch == -1:
                    return self.try_while_waiting()
            else:
                self.parent.curses_pad.timeout(-1)
                ch = self.parent.curses_pad.getch()
            # handle escape-prefixed rubbish.
            if ch == curses.ascii.ESC:
                #self.parent.curses_pad.timeout(1)
                self.parent.curses_pad.nodelay(1)
                ch2 = self.parent.curses_pad.getch()
                if ch2 != -1: 
                    ch = curses.ascii.alt(ch2)
                self.parent.curses_pad.timeout(-1) # back to blocking mode
                #curses.flushinp()
            
            self.handle_input(ch)
            self.try_adjust_widgets()

    #def when_parent_changes_value(self):
        # Can be called by forms when they chage their value.
        #pass

    def safe_string(self, this_string):
        """Check that what you are trying to display contains only
        printable chars.  (Try to catch dodgy input).  Give it a string,
        and it will return a string safe to print - without touching
        the original.  In Python 3 this function is not needed"""
        # In python 3
        if sys.version_info[0] >= 3:
            return this_string
        if this_string == None: 
            return ""
        elif not GlobalOptions.ASCII_ONLY:
            try:
                rtn_value = this_string.encode(locale.getpreferredencoding())
                return rtn_value
            except IndexError:
                pass
            except TypeError:
                pass
            except UnicodeDecodeError:
                warnings.warn("Unicode Error")
                raise
            except UnicodeEncodeError:
                pass
        rtn = self.safe_filter(this_string)
        return rtn
    
    def safe_filter(self, this_string):
        s = ''
        for cha in this_string:
            try:
                s += cha.encode('ascii')
            except:
                s += '?'
        return s
        
class DummyWidget(Widget):
    "This widget is invisible and does nothing.  Which is sometimes important."
    def __init__(self, screen, *args, **keywords):
        super(DummyWidget, self).__init__(screen, *args, **keywords)
        self.height = 0
        self.widget = 0
        self.parent = screen
    def display(self):
        pass
    def update(self, clear=False):
        pass
    def set_editable(self, value):
        if value: self._is_editable = True
        else: self._is_editable = False
    def get_editable(self):
        return(self._is_editable)
    def clear(self, usechar=' '):
        pass
    def calculate_area_needed(self):
        return 0,0


