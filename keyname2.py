#!/usr/bin/python
import curses
import curses.ascii

def mainloop(scr):
	while 1:
		scr.keypad(1)
		ch = scr.getch()
		try: 
			scr.erase()
			scr.addstr(0,0, "%s, %s,  %s" % 
			(curses.keyname(ch), curses.ascii.unctrl(ch), ch))
		except:
			pass
		scr.refresh()
	
if __name__ == "__main__":
	curses.wrapper(mainloop)
