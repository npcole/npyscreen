#!/usr/bin/python
import curses
import widget
import checkbox
import textbox

class MiniButton(checkbox.Checkbox):
	def __init__(self, screen, name='Button', *args, **keywords):
		self.name = name
		self.label_width = len(name) + 2
		super(MiniButton, self).__init__(screen, *args, **keywords)
		
	def calculate_area_needed(self):
		return 1, self.label_width+2

	def update(self, clear=True):
		if clear: self.clear()
		
		if self.value:
			self.parent.curses_pad.addstr(self.rely, self.relx, '>')
			self.parent.curses_pad.addstr(self.rely, self.relx+self.width-1, '<')
		
		if self.editing:
			button_state = curses.A_STANDOUT
		else:
			button_state = curses.A_NORMAL
		
		str = self.name.center(self.label_width)
		if self.do_colors():
			self.parent.curses_pad.addnstr(self.rely, self.relx+1, str, self.label_width, self.parent.theme_manager.findPair(self, 'CONTROL') | button_state)
		else:
			self.parent.curses_pad.addnstr(self.rely, self.relx+1, str, self.label_width, button_state) 
		

def testme(sa):
	import screen_area
	SA = screen_area.ScreenArea()
	w = MiniButton(SA, rely=3, relx=3)
	w.edit()
	w.display()
	curses.napms(1500)


if __name__ == '__main__':
	import curses.wrapper
	curses.wrapper(testme)
	print "Join me, and we will end this destructive conflict"
