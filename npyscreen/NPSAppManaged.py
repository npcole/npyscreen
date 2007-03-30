#!/usr/bin/env python
# encoding: utf-8
"""
NPSAppManaged.py
"""
import NPSApp
import Form
import weakref

class NPSAppManaged(NPSApp.NPSApp):
    """This class is intended to make it easier to program applications with many screens:
    
    1. The programmer should not now select which 'Form' to display himself.  Instead, he should set the NEXT_ACTIVE_FORM class variable.  
       See the addForm method for details.
       
       Doing this will avoid accidentally exceeding the maximum recursion depth.  Forms themselves should be placed under the management
       of the class using the 'addFrom' method.
       
    2. Forms that are managed by this class can access a proxy to the parent application through their ".parentApp" attribute, which is
       created by this class.
       
    3. Optionally, Forms managed by this class may be given an .activate method, which will be called instead of their .edit loop
    
    4. The method onInMainLoop is called after each screen has exited. This can be overridden. 
    
    5. This method should be able to see which screen was last active using the self._LAST_NEXT_ACTIVE_FORM attribute, which is only set
       just before each screen is displayed.
       
    6. Unless you override the attribute STARTING_FORM, the first form to be called should be named 'MAIN'
    
    7. Do override the onStart and onCleanExit functions if you wish.
    """

    STARTING_FORM = "MAIN"

    def __init__(self):
        super(NPSAppManaged, self).__init__()    
        self.NEXT_ACTIVE_FORM = self.__class__.STARTING_FORM
        self._LAST_NEXT_ACTIVE_FORM = None
        self._Forms = {}
    
    def addForm(self, name, fm):
        """name should be a string which should uniquely identify the form.  fm should be a Form."""
        fm.parentApp = weakref.proxy(self)
        self._Forms[name] = fm
        
    def removeForm(self, name):
        del self._Forms[name].parentApp
        del self._Forms[name]

    def main(self):
        """Call this function to start your application.  You should not override this function, but override the nInMainLoop, onStart and
        onCleanExit methods instead, if you need to modify the application's behaviour. 

        When this method is called, it will activate the form named by the class variable STARTING_FORM.  By default this Form will be called
        'MAIN'.  

        When that form exits (user selecting an ok button or the like), the form named by object variable NEXT_ACTIVE_FORM will be activated.

        If NEXT_ACTIVE_FORM is None, the main() loop will exit.
        
        The form selected will be edited using it's .edit() method UNLESS it has been provided with an .activate() method,
        in which case that method will be called instead.  This is done so that the same class of form can be made 
        NPSAppManaged aware and have the normal non-NPSAppManaged edit loop.
        
        Note that NEXT_ACTIVE_FORM is a string that is the name of the form that was specified when .addForm was called.
        """
        
        self.onStart()
        while self.NEXT_ACTIVE_FORM != "" and self.NEXT_ACTIVE_FORM != None:
            self._LAST_NEXT_ACTIVE_FORM = self._Forms[self.NEXT_ACTIVE_FORM]
            if hasattr(self._Forms[self.NEXT_ACTIVE_FORM], "activate"):
                self._Forms[self.NEXT_ACTIVE_FORM].activate()
            else:
                self._Forms[self.NEXT_ACTIVE_FORM].edit()
            
            self.onInMainLoop()
        self.onCleanExit()
        
    def onInMainLoop(self):
        """Called between each screen while the application is running. Not called before the first screen. Override at will"""
        
    def onStart(self):
        """Override this method to perform any initialisation."""
        pass
                
    def onCleanExit(self):
        """Override this method to perform any cleanup when application is exiting without error."""
        
def main(*args):
    import ActionForm
    import textbox
    
    class TestForm(ActionForm.ActionForm):
        def activate(self):
            self.edit()
            self.parentApp.NEXT_ACTIVE_FORM = None
    
    T = NPSAppManaged()
    a = TestForm()
    a.add(textbox.Textfield, name='Test')
    T.addForm('MAIN', a)
    T.main()


if __name__ == '__main__':
    import curses
    curses.wrapper(main)

