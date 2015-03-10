Writing Tests
=============

(New in version 4.7.0)

It is possible to script npyscreen application keyboard input for the purposes of testing.  

The npyscreen module exports the following dictionary containing the relevant settings::

    TEST_SETTINGS = {
        'TEST_INPUT': None,
        'TEST_INPUT_LOG': [],
        'CONTINUE_AFTER_TEST_INPUT': False,
        }

If 'TEST_INPUT' is None the application progresses normally.  If it is an array, keystrokes are loaded from the left hand side of the array and fed to the application in place of getting input from the keyboard.  Note that special characters such as *curses.KEYDOWN* can be handled, and control characters can be indicated by a string such as *"^X"*.

A keypress that is fed to the application in this way is automatically appended to *'TEST_INPUT_LOG'*, so it is possible to see where an error occurred when handling input.

If 'CONTINUE_AFTER_TEST_INPUT' is true, then after the automatic input has been specified, *'TEST_INPUT'* is set to *None* and the application continues normally.  If it is False, then the exception *ExhaustedTestInput* is raised instead.

Convenience Functions (new in version 4.8.5)
--------------------------------------------

.. py:function:: npyscreen.add_test_input_from_iterable(iterable)
	
	Add each item of `iterable` to `TEST_SETTINGS['TEST_INPUT']`.

.. py:function:: npyscreen.add_test_input_ch(ch)

	Add `ch` to `TEST_SETTINGS['TEST_INPUT']`.


Example
-------

The following is a trivial example::

    #!/usr/bin/python
    import curses
    import npyscreen
    import unittest

    npyscreen.TEST_SETTINGS['TEST_INPUT'] = [ch for ch in 'This is a test']
    npyscreen.TEST_SETTINGS['TEST_INPUT'].append(curses.KEY_DOWN)
    npyscreen.TEST_SETTINGS['CONTINUE_AFTER_TEST_INPUT'] = True

    class TestForm(npyscreen.Form):
        def create(self):
            self.myTitleText = self.add(npyscreen.TitleText, name="Events (Form Controlled):", editable=True)
    
    class TestApp(npyscreen.StandardApp):
        def onStart(self):
            self.addForm("MAIN", TestForm)
    

    if __name__ == '__main__':
        A = TestApp()
        A.run()