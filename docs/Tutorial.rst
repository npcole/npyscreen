========
Tutorial
========

This tutorial is a work-in-progress.

.. contents::

Part I: Forms, Widgets and Applications
***************************************

Using a wrapper
===============

Switiching into and out of a curses environment is a very boring task.  The python curses module provides a wrapper to do this, and this is exposed by npyscreen as wrapper_basic.  The basic framework for a very simple application looks like this::

    import npyscreen
    
    def myFunction(*args):
        pass
    
    if __name__ == '__main__':
        npyscreen.wrapper_basic(myFunction)
        print "Blink and you missed it!"
        
Which doesn't do anything clever.  The curses environment starts and exits without actually doing anything.  But it's a start.

Note that npyscreen also provides other wrappers that do slightly different things.


Using a Form
============

Now let's try putting something on the screen.  For that we need a *Form* instance::

    F = npyscreen.Form(name='My Test Application')

should do the trick.  Let's put that into our wrapper::

    import npyscreen
    
    def myFunction(*args):
        F = npyscreen.Form(name='My Test Application')
    
    if __name__ == '__main__':
        npyscreen.wrapper_basic(myFunction)
        print "Blink and you missed it!"

Which still seems to do nothing -- because we haven't actually displayed the Form.  *F.display()* would put it on the screen, but we actually want to let the user play with it, so let's do F.edit() instead::

    import npyscreen
    
    def myFunction(*args):
        F = npyscreen.Form(name='My Test Application')
        F.edit()
    
    if __name__ == '__main__':
        npyscreen.wrapper_basic(myFunction)
        print "Blink and you missed it!"
        
Which won't run, because when we try to edit the Form npyscreen discovers there's no widget to edit.  Let's put that right.

Adding the first widget
=======================

Let's put a textbox with a title in place.  We do that with the code::

    F.add(npyscreen.TitleText, name="First Widget")
    
The full code is::

    import npyscreen
    
    def myFunction(*args):
        F = npyscreen.Form(name='My Test Application')
        F.add(npyscreen.TitleText, name="First Widget")
        F.edit()
    
    if __name__ == '__main__':
        npyscreen.wrapper_basic(myFunction)
        print "Blink and you missed it!"
        
Much better! That gives us something looking like an application.  With just a three small changes we can change closing the message displayed to whatever the user typed::

    import npyscreen
    
    def myFunction(*args):
        F = npyscreen.Form(name='My Test Application')
        myFW = F.add(npyscreen.TitleText, name="First Widget")   # <------- Change 1
        F.edit()
        return myFW.value   # <------- Change 2
    
    if __name__ == '__main__':
        print npyscreen.wrapper_basic(myFunction)  # <---- and change 3

Let's be a little more object-oriented
======================================

The approach we've been using works fine for simple applications, but once we start creating lots of widgets on a form, it is better to tuck all of that code away inside a Form object.

Instead of using the base Form() class in a very procedural way, let's create our own Form class.  We'll override the Form's *create()* method, which is called whenever a Form is created::

    class myEmployeeForm(npyscreen.Form):
        def create(self):
            super(myEmployeeForm, self).create()  # This line is not strictly necessary: the API promises that the create method does nothing by default.
                                                  # I've ommitted it from later example code.
            self.myName        = self.add(npyscreen.TitleText, name='Name')
            self.myDepartment  = self.add(npyscreen.TitleText, name='Department')
            self.myDate        = self.add(npyscreen.TitleDateCombo, name='Date Employed')
            
We can use our wrapper code from before to use it::

    import npyscreen
    
    class myEmployeeForm(npyscreen.Form):
        def create(self):
            self.myName        = self.add(npyscreen.TitleText, name='Name')
            self.myDepartment  = self.add(npyscreen.TitleText, name='Department')
            self.myDate        = self.add(npyscreen.TitleDateCombo, name='Date Employed')
    
    def myFunction(*args):
        F = myEmployeeForm(name = "New Employee")
        F.edit()
        return "Created record for " + F.myName.value
    
    if __name__ == '__main__':
        print npyscreen.wrapper_basic(myFunction)
    


Offering Choice
===============

Actually, we probably don't want just any old department name typed in - we want to offer a list of choices.  Let's use the TitleSelectOne widget.  It's a multi-line widget, so we need to take care that it takes up only a few lines of the screen (left to itself it would take up all the remaining space on the screen)::

    self.myDepartment = self.add(npyscreen.TitleSelectOne, max_height=3, 
                                    name='Department', 
                                    values = ['Department 1', 'Department 2', 'Department 3'],
                                    scroll_exit = True  # Let the user move out of the widget by pressing the down arrow instead of tab.  Try it without 
                                                        # to see the difference.
                                    )
    
Putting that in context::

        import npyscreen

        class myEmployeeForm(npyscreen.Form):
            def create(self):
                self.myName        = self.add(npyscreen.TitleText, name='Name')
                self.myDepartment = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3, name='Department', values = ['Department 1', 'Department 2', 'Department 3'])
                self.myDate        = self.add(npyscreen.TitleDateCombo, name='Date Employed')

        def myFunction(*args):
            F = myEmployeeForm(name = "New Employee")
            F.edit()
            return "Created record for " + F.myName.value

        if __name__ == '__main__':
            print npyscreen.wrapper_basic(myFunction)
            
            

Being Even More Object-Oriented
===============================

What we've done so far is all very well, but still ugly at the edges.  We're still calling F.edit() ourselves, which is fine in a single-form application, but could lead to problems with recursion-depth later if we are not careful.  Fortunately, npyscreen can manage the display and editing of Forms.  We need to use the *NPSAppManaged* class.

Let's scrap the framework that has supported us so far, and start with a different basis for our application::

    import npyscreen

    class MyApplication(npyscreen.NPSAppManaged):
        pass

     if __name__ == '__main__':
        TestApp = MyApplication().run()
        print "All objects, baby."
          
Which will exit with an exception, because you have no 'MAIN' Form, which is the starting point for all NPSAppManaged applications.

Let's put that right.  We'll use the Form class from before::
    
    import npyscreen

    class myEmployeeForm(npyscreen.Form):
        def create(self):
           self.myName        = self.add(npyscreen.TitleText, name='Name')
           self.myDepartment = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3, name='Department', values = ['Department 1', 'Department 2', 'Department 3'])
           self.myDate        = self.add(npyscreen.TitleDateCombo, name='Date Employed')

   class MyApplication(npyscreen.NPSAppManaged):
       def onStart(self):
           self.addForm('MAIN', myEmployeeForm, name='New Employee')

   if __name__ == '__main__':
       TestApp = MyApplication().run()
       print "All objects, baby."
    
If you run the above code, you'll find yourself frustrated, because the application will continually display the form for you to edit, and you'll have to press "^C" (Control C) to exit.

That's because the NPSAppManaged class continually displays whatever form is named by its NEXT_ACTIVE_FORM attribute (in this case, the default - 'MAIN').

Let's alter the myEmployeeForm to tell it that after being run in an NPSAppManaged context, it should tell its NPSAppManaged parent to stop displaying Forms.  We do that by creating the special method called *afterEditing*::

    class myEmployeeForm(npyscreen.Form):
        def afterEditing(self):
            self.parentApp.NEXT_ACTIVE_FORM = None
    
        def create(self):
           self.myName        = self.add(npyscreen.TitleText, name='Name')
           self.myDepartment = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3, name='Department', values = ['Department 1', 'Department 2', 'Department 3'])
           self.myDate        = self.add(npyscreen.TitleDateCombo, name='Date Employed')

    
    
If we preferred, we could achieve the same result by defining a special method *onInMainLoop* in our MyApplication class - this method would get called after each form has been edited. 

Our code now looks like this::
    
    import npyscreen

    class myEmployeeForm(npyscreen.Form):
        def afterEditing(self):
            self.parentApp.NEXT_ACTIVE_FORM = None

        def create(self):
           self.myName        = self.add(npyscreen.TitleText, name='Name')
           self.myDepartment = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3, name='Department', values = ['Department 1', 'Department 2', 'Department 3'])
           self.myDate        = self.add(npyscreen.TitleDateCombo, name='Date Employed')

    class MyApplication(npyscreen.NPSAppManaged):
       def onStart(self):
           self.addForm('MAIN', myEmployeeForm, name='New Employee')
           # A real application might define more forms here.......
           
    if __name__ == '__main__':
       TestApp = MyApplication().run()
  
  
Choosing an approach
====================

The last example above is probably over-kill for a very simple application.  But it provides a much more robust framework with which to build larger applications than the framework we used at the start of the tutorial, at the cost of only a few lines of code.  If you are displaying more than one screen, or running an application continuously, this is probably the approach you should take.