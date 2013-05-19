# encoding: utf-8

import curses
import os
import sys
import termios
import fcntl
import struct

def main(screen):
	while 1:
		y, x = struct.unpack('hh', fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, 'xxxx'))
		win = curses.newwin(y-1, x-2, 0,0)
		#y, x = win.getmaxyx()

		win.addstr("Terminal Size = %s x %s" % (y, x))
		win.refresh()
		curses.napms(100)


if __name__ == '__main__':
	curses.wrapper(main)

