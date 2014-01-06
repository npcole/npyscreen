All about Key Bindings
======================

What is going on
****************

Many objects can take actions based on user key presses.  All such objects inherit from the internal class InputHandler.  That class defines a dictionary called *handlers* and a list called *complex_handlers*.  Both of these are set up by a method called *set_up_handlers* called during the Constructor.

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
