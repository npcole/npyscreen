#!/usr/bin/env python
# encoding: utf-8
import curses.wrapper
import locale

def wrapper(call_function):
	#set the locale properly
	locale.setlocale(locale.LC_ALL, '')
	return curses.wrapper(call_function)
    