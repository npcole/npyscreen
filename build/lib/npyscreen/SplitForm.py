#!/usr/bin/python
import Form

class SplitForm(Form):
	pass
	

def testme(scr):
	print "Only now, at the end"

if __name__ == "__main__":
	import curses.wrapper
	curses.wrapper(testme)
