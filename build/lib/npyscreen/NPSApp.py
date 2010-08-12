#!/usr/bin/env python
import curses
import curses.wrapper
import _curses

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

	def run(self):
		"""Run application.  Calls Mainloop wrapped properly."""
		try:
			curses.longname() # Test if curses is already running.
			if curses.isendwin(): 
			    raise AlreadyOver
			return self.main()
		except AlreadyOver:
			return curses.wrapper(self.__remove_argument_call_main)
		#except NameError:
		#	return curses.wrapper(self.__remove_argument_call_main)
		except _curses.error:
			return curses.wrapper(self.__remove_argument_call_main)


if __name__ == '__main__':
	App = NPSApp(); App.run()
	print "A Jedi, who was a pupil of mine..."
