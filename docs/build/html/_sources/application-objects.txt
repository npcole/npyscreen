Application Objects
===================

.. py:class: NPSAppManaged

NPSAppManaged provides a framework to start and end your application and to manage the display of the various Forms that you have created, in a way that should not create recursion depth problems.

Unless you have exceptionally good reasons to do otherwise, *NPSAppManaged* is almost certainly the best way to manage your application.  

Unlike the plain NPSApp class, you do not need to write your own main loop - *NPSAppManaged* will manage the display of each Form of your application.  Set up your form objects and simply call the *.run()* method of your NPSAppManaged instance.

Letting NPSAppManaged manage your Forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are three methods for registering a Form object with an NPSAppManaged instance:

    
.. py:method:: NPSAppManaged.addForm(*id*, *FormClass*, ...)

    This version creates a new form and registers it with the NPSAppManaged instance.  It returns a weakref.proxy to the form object.  *id* should be a string that uniquely identifies the Form.  *FormClass* should be the class of form to create.  Any additional arguments will be passed to the Form's constructor.  Use this version if you are not storing a separate reference to your form elsewhere.

.. py:method:: NPSAppManaged.addFormClass(*id*, *FormClass* ...)

    This version registers a class of form rather than an instance.  A new instance will be created every time it is edited.  Additional arguements will be passed to the form's constructor every time it is created.

.. py:method:: NPSAppManaged.registerForm(id, fm)

    *id* should be a string that uniquely identifies the form.  *fm* should be a Form object.  Note that this version only stores a weakref.proxy inside NPSAppManaged - in contrast to the .addForm version.


All Forms registered with an NPSAppManaged instance can access the controlling application as *self.parentApp*.

If for any reason you need to remove a Form, you can do with the `.removeForm(*id*)` method. 

Running an NPSApplicationManaged application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:method:: run
	
	Start an NPSAppManaged application mainloop.  This method will activate the default form, which should have been given an id of "MAIN".

.. py:attribute:: NPSAppManaged.STARTING_FORM 

	If for any reason you need to change the name of the default form, you can change it here.
	
Once an application is running, the following methods control which form is presented to the user.

.. py:method:: NPSAppManaged.setNextForm(formid)
	
	Set the form to be displayed when the current one exits.

.. py:method:: NPSAppManaged.setNextFormPrevious

	Set the form to be displayed when the current one exits to the previous one in the history

.. py:method:: NPSAppManaged.switchForm(formid)

	Immediately switch to the named form, bypassing any exit logic of the current form. 

.. py:method:: NPSAppManaged.switchFormPrevious()

    Immediately switch to the previous form in the history.


In detail
+++++++++

Once all of your forms are ready and registered with an NPSAppManaged instance, you should call .run()

This method will activate the default form, which should have been given an id of "MAIN".  You can change this default by changing the class/instance variable `.STARTING_FORM`.

Thereafter, the next form to be displayed will be the one specified by the instance variable *NEXT_ACTIVE_FORM*.  Whenever a Form edit loop exits, the Form specified here will be activated.  If *NEXT_ACTIVE_FORM* is None, the main loop will exit.  *NEXT_ACTIVE_FORM* should be set by calling the application's *setNextForm(formid)* method.  This documentation used to suggest that you set the attribute directly. While there are no immediate plans to deprecate this attribute, setting it directly should be avoided.

There are three mechanisms that Forms should use to control `NEXT_ACTIVE_FORM`.  

1. All Forms registered with an NPSAppManaged which do *not* have the special method *.activate()* will have their method *.afterEditing* called, if they have it.  Logic to determine which the *NEXT_ACTIVE_FORM* should be should go here.  *NEXT_ACTIVE_FORM* should be set by calling the application's *setNextForm(formid)* method.  If you are expecting your users to select an ok or cancel button, this is the preferred way to switch screens.

2. The application method *switchForm(formid)* causes the application to immediately stop editing the current form and switch to the one specified. Depending on the type of Form, the logic associated with them may be bypassed too.

3. Forms registered with an NPSAppManaged may be given an *.activate()* method, which NPSAppManaged will call instead of the usual *.edit()* method.  This can contain additional logic.  This is NOT the preferred method, but may allow greater flexibility.  Note that in this case, the usual .edit() method will not be called, unless you call it explicitly.   For example, an .activate() method might look like this::
    
    def activate(self):
         self.edit()
         self.parentApp.setNextForm(None)
    
   which would cause the mainloop to exit after the Form was complete.

Additional Services offered by NPSAppManaged
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following methods may be usefully overridden by subclassing NPSAppManaged.  By default they do nothing.

.. py:method:: NPSAppManaged.onInMainLoop 
    
	Called between each screen while the application is running. Not called before the first screen. 

.. py:method:: NPSAppManaged.onStart

	Override this method to perform any initialisation.  If you wish, you can set up your application's Forms here.
        
.. py:method:: NPSAppManaged.onCleanExit

    Override this method to perform any cleanup when application is exiting without error.

.. py:attribute:: NPSAppManaged.keypress_timeout_default

    If this is set, new forms will be created with keypress_timeout set to this, provided they know what application they belong to - i.e. they have been passed *parentApp=* at creation time. If you are using NPSAppManaged, this will happen automatically.
	
.. py:method:: NPSAppManaged.while_waiting

	Applications can also have a *while_waiting* method.  You can define and override this at will, and it will be called while the application is waiting for user input (see the while_waiting method on forms). 

.. py:method:: NPSAppManaged._internal_while_waiting

	This method is for internal use by npyscreen.

.. py:method:: NPSAppManaged.switchForm(formid)

    Immediately stop editing the current form and switch to the specified form.

.. py:method:: NPSAppManaged.switchFormPrevious()

    Immediately switch to the previous form in the history.

.. py:method:: NPSAppManaged.resetHistory

    Forget the previous forms visted.

.. py:method:: NPSAppManaged.getHistory

    Get a list of the Forms visited


Methods and attributes on Forms managed by this class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Forms called by NPSAppManaged can be given the methods

.. py:method:: Form.beforeEditing()

    called before the edit loop of the form is called

.. py:method:: Form.afterEditing()

    called when the form is exited

.. py:method:: Form.activate()

    The presence of this method entirely overrides the existing .beforeEditing .edit  and afterEditing methods.
    

.. py:attribute::parentApp

    Forms created by the NPSAppManaged class have an attribute `parentApp` which is a reference back to their controlling application. 





Other Application classes
=========================


.. py:class::  NPSApp

To use NPSApp subclass it and provide your own `.main()` definition.  When you are ready to run the application call `.run()` and your mainloop will be executed.

While it provides maximum flexibility, NPSApp is in almost every other way inferior to NPSAppManaged.  Do not use it for new projects, and reguard it as an internal base class only.
