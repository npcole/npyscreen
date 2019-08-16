Enhancing Mouse Support
=======================
Widgets that wish to handle mouse events in more detail should override the method *.handle_mouse_event(self, mouse_event)*.  Note that *mouse_event* is a tuple::
    
    def handle_mouse_event(self, mouse_event):
        mouse_id, x, y, z, bstate = mouse_event # see note below.
        # Do things here....

This is mostly useful, but x and y are absolute positions, rather than relative ones.  For that reason, you should use the convenience function provided to convert these values into co-ordinates relative to the widget.  Thus, most mouse handling functions will look like this::

    def handle_mouse_event(self, mouse_event):
        mouse_id, rel_x, rel_y, z, bstate = self.interpret_mouse_event(mouse_event)
        # Do things here.....
    
The mouse handler will only be called if the widget is "editable".  In very rare cases, you may wish to have a non-editable widget respond to mouse events.  In that case, you can set the widget's attribute *.self.interested_in_mouse_even_when_not_editable* to True.

See the Python Library curses module documentation for more detail on mouse events.
