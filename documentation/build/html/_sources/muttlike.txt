Writing More Complex Forms
==========================

A very typical style of programming for terminal applications has been to have a screen that has a command line, typically at the bottom of the screen, and then some kind of list widget or other display taking up most of the screen, with a title bar at the top and a status bar above the command line.  Variations on this scheme are found in applications like Mutt, less, Vim, irssi and so on.

To make writing these kinds of form easier, npyscreen provides a series of classes that are intended to work together.

FormMuttActive, FormMuttActiveWithMenus, FormMuttActiveTraditional, FormMuttActiveTraditionalWithMenus
    These classes define the basic form.  The following *class attributes* dictate exactly how the form is created::
            
            MAIN_WIDGET_CLASS   = wgmultiline.MultiLine
            MAIN_WIDGET_CLASS_START_LINE = 1
            STATUS_WIDGET_CLASS = wgtextbox.Textfield
            STATUS_WIDGET_X_OFFSET = 0
            COMMAND_WIDGET_CLASS= wgtextbox.Textfield
            COMMAND_WIDGET_NAME = None
            COMMAND_WIDGET_BEGIN_ENTRY_AT = None
            COMMAND_ALLOW_OVERRIDE_BEGIN_ENTRY_AT = True
    
            DATA_CONTROLER    = npysNPSFilteredData.NPSFilteredDataList
            
            ACTION_CONTROLLER  = ActionControllerSimple
    
    The default definition makes the following instance attributes available after initalization::
            
            # Widgets - 
            self.wStatus1 # by default a title bar
            self.wStatus2 # just above the command line
            self.wMain    # the main area of the form - by default a MultiLine object
            self.wCommand # the command widget
            
            self.action_controller # not a widget. See below.
    
    The form's *.value* attribute is set to an instance of the object specified by DATA_CONTROLLER.
    
    Typically, and application will want to define its own DATA_CONTROLLER and ACTION_CONTROLLER.
    
    The difference between the traditional and non-traditional forms is that in the traditional form, the focus stays always with the command line widget, although some keypresses will be passed to the MAIN_WIDGET_CLASS - so that, from the user's point of view, it looks as if he/she is interacting with both at once.
    
TextCommandBox
    The TextCommandBox is like a usual text box, except that it passes what the user types to the action_controller.  In addition, it can keep a history of the commands entered.  See the documentation on ActionControllerSimple for more details.
    
TextCommandBoxTraditional
    This is the same as the TextCommandBox, except that it additionally will pass certain keystrokes to the widget specified by *self.linked_widget*.  In the default case, any keystroke that does not match a handler in TextCommandBoxTraditional will be passed to the linked widget.  Additionally, any keystroke that is listed in the list *self.always_pass_to_linked_widget* will be handled by the linked widget.  However, if the current command line begins with any character that is listed in the class attribute *BEGINNING_OF_COMMAND_LINE_CHARS*, the user input will be handled by this class, not by the linked widget.
    
    This is rather complicated, but an example will make it clearer.  The default BEGINNING_OF_COMMAND_LINE_CHARS specifies that ':' or '/' marks the beginning of a command.  After that point, keypresses are handled by this widget, not by the linked widget, so that the up and down arrows start to navigate the command history.  However, if the command line is currently empty, those keys navigate instead the linked widget.  
    
    As in the TextCommandBox widget, the value of the command line is passed to the parent form's action_controller object.
    
ActionControllerSimple
    This object receives command lines and executes call-back functions.  
    
    It recognises two types of command line - a "live" command line, where an action is taken with every change in the command line, and a command that is executed when the return key is pressed.
    
    Callbacks are added using the *add_action(ident, function, live)*, method.  'ident' is a regular expression that will be matched against the command line, *function* is the callback itself and *live* is either True or False, to specify whether the callback should be executed with every keypress (assuming that 'ident' matches).
    
    Command lines that match the regular expression 'ident' cause the call-back to be called with the following arguments: *call_back(command_line, control_widget_proxy, live=True)*.  Here *command_line* is the string that is the command line, *control_widget_proxy* is a weak reference to the command line widget, and live specifies whether the function is being called 'live' or as a result of a return.  
    
    The method *create()* can be overridden. It is called when the object is created. The default does nothing.  You probably want to use this as a place to call *self.add_action*.

NPSFilteredDataBase
    The default *NPSFilteredDataBase* class suggests how the code to manage the display might be separated out into a separate object.  The precise methods will be very application dependent.  This is not an essential part of this kind of application, but it is good practice to keep the logic of (for example) database access separate from the logic of the user interface.



Example Code
************

The following example shows how this model works.  The application creates an ActionController that has a search action.  This action calls the user-defined function set_search, which communicates with the Form's parent.value (actually a NPSFilteredDataBase class). It then uses this class to set the values in wMain.values and calls wMain.display() to update the display.

FmSearchActive is simply a FormMuttActiveTraditional class, with a class attribute that specifies that the form should use our action controller::
    
    class ActionControllerSearch(npyscreen.ActionControllerSimple):
        def create(self):
            self.add_action('^/.*', self.set_search, True)
    
        def set_search(self, command_line, widget_proxy, live):
            self.parent.value.set_filter(command_line[1:])
            self.parent.wMain.values = self.parent.value.get()
            self.parent.wMain.display()


    class FmSearchActive(npyscreen.FormMuttActiveTraditional):
        ACTION_CONTROLLER = ActionControllerSearch

    class TestApp(npyscreen.NPSApp):
        def main(self):
            F = FmSearchActive()
            F.wStatus1.value = "Status Line "
            F.wStatus2.value = "Second Status Line "
            F.value.set_values([str(x) for x in range(500)])
            F.wMain.values = F.value.get()
        
            F.edit()


    if __name__ == "__main__":
        App = TestApp()
        App.run()
