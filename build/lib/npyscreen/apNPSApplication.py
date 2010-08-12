#!/usr/bin/env python
import curses
import locale
import _curses

from . import npyssafewrapper


class AlreadyOver(Exception):
    pass

class NPSApp(object):
    _run_called = 0
    def main(self):
        """Overload this method to create your application"""

    def __remove_argument_call_main(self, screen):
        # screen disgarded.
        del screen
        return self.main()

    def run(self, fork=None):
        """Run application.  Calls Mainloop wrapped properly."""
        if fork is None:
            return npyssafewrapper.wrapper(self.__remove_argument_call_main)
        else:
            return npyssafewrapper.wrapper(self.__remove_argument_call_main, fork=fork)
