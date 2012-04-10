#!/usr/bin/python
import curses
import curses.ascii
#import locale

def mainloop(scr):
	while 1:
		scr.keypad(1)
		curses.halfdelay(100)
		ch = scr.getch()
		if ch == "-1": scr.addstr(2, 0, '-1')
		try: 
			scr.erase()
			scr.addstr(0,0, "%s, %s,  %s" % 
			(curses.keyname(ch), curses.ascii.unctrl(ch), ch))
			scr.addstr(1,0, str(ch))
		except:
			raise
		#return ch
		#scr.addstr(2,2, unicode(ch, 'utf-8'))
		scr.refresh()
	
if __name__ == "__main__":
#	locale.setlocale(locale.LC_ALL, '')
	print(curses.wrapper(mainloop))
