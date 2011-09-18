#!/usr/bin/python
import curses
import curses.ascii
import locale

def mainloop(scr):
	curses.mousemask(curses.ALL_MOUSE_EVENTS)
	while 1:
		#scr.keypad(1)
		#curses.halfdelay(1)
		ch = scr.getch()
		#if ch == "-1": scr.addstr(2, 0, '-1')
		scr.addstr(2, 0, str(ch))
		#scr.erase()
		if ch == curses.KEY_MOUSE:
		    scr.addstr(4,0, "%s" % ' '.join(str(curses.getmouse())))
		#return ch
		scr.refresh()
	
if __name__ == "__main__":
	locale.setlocale(locale.LC_ALL, '')
	print curses.wrapper(mainloop)

