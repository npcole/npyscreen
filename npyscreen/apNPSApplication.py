#!/usr/bin/env python
import curses
import locale
import _curses

from . import npyssafewrapper


class AlreadyOver(Exception):
    pass




class NPSApp(object):
    _initscr_not_done = True

    def main(self):
        """Overload this method to create your application"""

    def __init__(self, enable_mouse=True, enable_colors=True):
        self._enable_mouse = enable_mouse
        self._enable_colors = enable_colors
        self._screen = None
        self._fork = False

    def resize(self):
        pass

    def _wrapped_startup(self):
        if self._fork or NPSApp._initscr_not_done:
            NPSApp._initscr_not_done = False
            locale.setlocale(locale.LC_ALL, '')
            self._screen = curses.initscr()
            try:
                curses.start_color()
            except:
                pass

        curses.noecho()
        curses.cbreak()
        self._screen.keypad(True)
        if self._fork:
            curses.def_prog_mode()
            curses.reset_prog_mode()

        if self._enable_mouse:
            curses.mousemask(curses.ALL_MOUSE_EVENTS)

        try:
            return_code = self.main()
        finally:
            self._screen.keypad(False)
            curses.echo()
            curses.nocbreak()
            curses.endwin()

        return return_code

    def run(self, fork=None):
        """Run application.  Calls Mainloop wrapped properly."""
        self._fork = fork
        if fork is None:
            return npyssafewrapper.wrapper(self._wrapped_startup)
        else:
            return npyssafewrapper.wrapper(self._wrapped_startup, fork=fork)
