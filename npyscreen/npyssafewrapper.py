#!/usr/bin/env python
# encoding: utf-8
import curses
import _curses
#import curses.wrapper
import locale
import os
#import pty
import subprocess
import sys
import warnings


def wrapper_basic(call_function):
    #set the locale properly
    locale.setlocale(locale.LC_ALL, '')
    return curses.wrapper(call_function)

#def wrapper(call_function):
#   locale.setlocale(locale.LC_ALL, '')
#   screen = curses.initscr()
#   curses.noecho()
#   curses.cbreak()
#   
#   return_code = call_function(screen)
#   
#   curses.nocbreak()
#   curses.echo()
#   curses.endwin()

def wrapper(call_function, fork=None):

    if fork:
        wrapper_fork(call_function)
    else:
        wrapper_no_fork(call_function)

def wrapper_fork(call_function, reset=True):
    pid = os.fork()
    if pid:
        # Parent
        os.waitpid(pid, 0)
        if reset:
            external_reset()
    else:

        return_code = call_function()

        sys.exit(0)

def external_reset():
    subprocess.call(['reset', '-Q'])
    
def wrapper_no_fork(call_function, reset=False):

    return_code = call_function()

    if reset:
        external_reset()

    return return_code
