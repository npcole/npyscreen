Displaying Brief Messages and Choices
=====================================

The following functions allow you to display a brief message or choice to the user.

.. py:function:: notify(message, title="Message", form_color='STANDOUT', wrap=True, wide=False,)

    This function displays a message on the screen.  It does not block and the user cannot interact with it - use it to display messages like "Please Wait" while other things are happening.
    
.. py:function:: notify_wait(message, title="Message", form_color='STANDOUT', wrap=True, wide=False,)
    
	This function displays a message on the screen, and blocks for a brief amount of time. The user cannot interact with it.
    
.. py:function:: notify_confirm(message, title="Message", form_color='STANDOUT', wrap=True, wide=False, editw=0)
    
    Display a message and an OK button.  The user can scroll the message if needed.  editw controls which widget is selected when the dialog is first displayed; set to 1 to have the OK button active immediately.
    
.. py:function:: notify_ok_cancel(message, title="Message", form_color='STANDOUT', wrap=True, editw = 0,)

    Display a message and return True if the user selected 'OK' and False if the user selected 'Cancel'.
    
.. py:function:: notify_yes_no(message, title="Message", form_color='STANDOUT', wrap=True, editw = 0)

    Similar to *notify_ok_cancel* except the names of the buttons are 'Yes' and 'No'.  Returns True or False.
    

The following function will display a dialog box for the user to select a filename.

.. py:function:: selectFile(select_dir=False, must_exist=False, confirm_if_exists=True,sort_by_extension=True,)

    This form is currently experimental.  The return value is the name of the file.
    
Blanking the Screen
===================

.. py:function:: blank_terminal()

    This function blanks the terminal.  It may sometimes be needed if Forms are being displayed that do not fill the whole screen.
