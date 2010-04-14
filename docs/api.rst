#############
Npyscreen API
#############

"User interfaces without all that mucking around in hyperspace"

***This Document is not only unfinished, but hardly written!***



.. contents::

Importing the Library
=====================

Import the library using::

    import npyscreen


Creating an Application
=======================

Most applications should subclass ``NPSAppManaged``

NPSAppManaged API
-----------------

The following methods control the flow of the application:

main()
    Call this function to start your application.  You should not override this function, but override the onInMainLoop, onStart and onCleanExit methods instead, if you need to modify the application's behaviour. 

    When this method is called, it will activate the form named by the class variable STARTING_FORM.  By default this Form will be called 'MAIN'.  

    When that form exits (user selecting an ok button or the like), the form named by object variable NEXT_ACTIVE_FORM will be activated.

    If NEXT_ACTIVE_FORM is None, the main() loop will exit.
    
    The form selected will be edited using it's .edit() method UNLESS it has been provided with an .activate() method, in which case that method will be called instead.  This is done so that the same class of form can be made NPSAppManaged aware and have the normal non-NPSAppManaged edit loop.
    
    After a Form has been edited, if it has an .afterEditing method, this will be called, unless it was invoked with the activate() method.A similar .beforeEditing method will be called if it exists before editing the form.  Again, the presence of a .activate method
    will override this behaviour.
    
    Note that NEXT_ACTIVE_FORM is a string that is the name of the form that was specified when . addForm .registerForm was called.
    
onStart()
    Override this method to perform any initialisation.  This will be called before any of the forms of your application are displayed.

onCleanExit()
    Override this method to perform any cleanup when application is exiting without error.
    
onInMainLoop()
    Called between each screen while the application is running. Not called before the first screen. Override at will.
    
setNextForm(form_id)
    Set the form that will be selected when the current one exits.

switchForm(form_id)
    Immediately switch to the form specified by form_id.
    
The following methods specify the forms that will be managed by the application:

``addForm(f_id, FormClass, *args, **keywords)``
    Create a form of the given class. f_id should be a string which will uniquely identify the form. ``args`` and ```keywords`` will be passed to the Form constructor.  Forms created in this way are handled entirely by the NPSAppManaged class.  A weak reference to the form will be returned.
    
registerForm(f_id, fm)
    f_id should be a string which should uniquely identify the form.  fm should be a Form.  Most of the time, ``addForm`` is more appropriate. 

removeForm(f_id)
    remove a form.  f_id is the string used to uniquely identify the form.
