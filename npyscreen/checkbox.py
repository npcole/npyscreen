#!/usr/bin/python

from textbox import Textfield
from widget import Widget
import widget
import curses

class Checkbox(Widget):

	False_box = '[ ]'
	True_box  = '[X]'
	
	def __init__(self, screen, value = False, **keywords):
		self.value = value
		super(Checkbox, self).__init__(screen, **keywords)
		
		self.label_area = Textfield(screen, rely=self.rely, relx=self.relx+5, 
					  width=self.width-5, value=self.name)

		self.show_bold = False
		self.highlight = False
		self.hide      = False

	def update(self, clear=True):
		if clear: self.clear()
		if self.hide: return True

		self.label_area.value = self.name
		
		if self.value:
			self.parent.curses_pad.addstr(self.rely, self.relx, self.__class__.True_box)
		else:
			self.parent.curses_pad.addstr(self.rely, self.relx, self.__class__.False_box)


		if self.editing:
			self.label_area.highlight = True
		else:
			self.label_area.highlight = False
		
		if self.show_bold: 
			self.label_area.show_bold = True
		else: 
			self.label_area.show_bold = False

		if self.highlight: 
			self.label_area.highlight = True
		else: 
			self.label_area.highlight = False

		self.label_area.update(clear=clear)
		
	def calculate_area_needed(self):
		return 1,0

	def set_up_handlers(self):
		super(Checkbox, self).set_up_handlers()
		
		self.handlers.update({
				curses.ascii.SP: self.h_toggle,
				ord('x'):	 self.h_toggle,
				curses.ascii.NL: self.h_select_exit,
			})
	
	def h_toggle(self, ch):
		if self.value is False or self.value is None or self.value == 0: 
			self.value = True
		else: 
			self.value = False
	
	def h_select_exit(self, ch):
		self.value = True
		self.editing = False
		self.how_exited = widget.EXITED_DOWN
		
class RoundCheckBox(Checkbox):
	False_box = '( )'
	True_box  = '(X)'

def testme(sa):
	import screen_area
	A = screen_area.ScreenArea()
	#w = Checkbox(A, rely=10, relx=10, name='Check Box')
	#w.display()
	w2 = Checkbox(A, relx = 3, name='Check Box')
	w2.display()
	curses.napms(1500)

if __name__ == '__main__':
	import curses.wrapper
	curses.wrapper(testme)
	print "Use the force"
