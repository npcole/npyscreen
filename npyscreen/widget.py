#!/usr/bin/python


import curses
import curses.ascii
import curses.wrapper
import weakref
import GlobalOptions


EXITED_DOWN  =  1
EXITED_UP    = -1
EXITED_LEFT  = -2
EXITED_RIGHT =  2
EXITED_ESCAPE= 127
EXITED_MOUSE = 130

class InputHandler(object):
	"An object that can handle user input"

	def handle_input(self, input):
		"""Returns True if input has been dealt with, and no further action needs taking.
		First attempts to look up a method in self.input_handers (which is a dictionary), then
		runs the methods in self.complex_handlers (if any), which is an array of form (test_func, dispatch_func).
		If test_func(input) returns true, then dispatch_func(input) is called. Check to see if parent can handle.
		No further action taken after that point."""
		
		if self.handlers.has_key(input):
			self.handlers[input](input)
			return True

		elif self.handlers.has_key(curses.ascii.unctrl(input)):
			self.handlers[curses.ascii.unctrl(input)](input)
			return True


		else:
			if not hasattr(self, 'complex_handlers'): return False
			for test, handler in self.complex_handlers:
				if test(input): 
					handler(input)
					return True
		if hasattr(self, 'parent') and hasattr(self.parent, 'handle_input'):
			if self.parent.handle_input(input):
				return True

		else:
			pass

	# If we've got here, all else has failed, so:
		return False

	def set_up_handlers(self):
		"""This function should be called somewhere during object initialisation (which all library-defined widgets do). You might like to override this in your own definition,
but in most cases the add_handers or add_complex_handlers methods are what you want."""
		#called in __init__
		self.handlers = {curses.ascii.NL:  self.h_exit_down,
	                       curses.ascii.CR:  self.h_exit_down,
			       curses.ascii.TAB: self.h_exit_down,
			       curses.KEY_DOWN:  self.h_exit_down,
			       curses.KEY_UP:    self.h_exit_up,
			       curses.KEY_LEFT:  self.h_exit_left,
			       curses.KEY_RIGHT: self.h_exit_right,
			       "^P":		        self.h_exit_up,
			       "^N":		        self.h_exit_down,
			       curses.ascii.ESC:	self.h_exit_escape,
			       curses.KEY_MOUSE:	self.h_exit_mouse,
			       }

		self.complex_handlers = []

	def add_handlers(self, handler_dictionary):
		"""Update the dictionary of simple handlers.  Pass in a dictionary with keyname (eg "^P" or curses.KEY_DOWN) as the key, and the function that key should call as the values """
		self.handlers.update(handler_dictionary)
	
	def add_complex_handlers(self, handlers_list):
		"""add complex handlers: format of the list is pairs of
		(test_function, callback) sets"""

		for pair in handlers_list:
			assert len(pair) == 2
		self.complex_handlers.extend(handlers_list)

###########################################################################################
# Handler Methods here - npc convention - prefix with h_

	def h_exit_down(self, input):
		"""Called when user leaves the widget to the next widget"""
		self.editing = False
		self.how_exited = EXITED_DOWN
		
	def h_exit_right(self, input):
		self.editing = False
		self.how_exited = EXITED_RIGHT

	def h_exit_up(self, input):
		"""Called when the user leaves the widget to the previous widget"""
		self.editing = False
		self.how_exited = EXITED_UP
		
	def h_exit_left(self, input):
		self.editing = False
		self.how_exited = EXITED_LEFT
		
	def h_exit_escape(self, input):
		self.editing = False
		self.how_exited = EXITED_ESCAPE

	def h_exit_mouse(self, input):
		self.editing = False
		self.how_exited = MOUSE_EVENT
	

class Widget(InputHandler):
	"A base class for widgets. Do not use directly"

	def destroy(self):
		"""Destroy the widget: methods should provide a mechanism to destroy any references that might
		case a memory leak.  See select. module for an example"""
		pass

	def __init__(self, screen, 
			relx=0, rely=0, name=None, value=None, 
			width = False, height = False,
			max_height = False, max_width=False,
			editable=True,
			hidden=False,
			color='DEFAULT',
			**keywords):
		"""The following named arguments may be supplied:
		name= set the name of the widget.
		width= set the width of the widget.
		height= set the height.
		max_height= let the widget choose a height up to this maximum.
		max_width=  let the widget choose a width up to this maximum.
		editable=True/False the user may change the value of the widget.
		hidden=True/False The widget is hidden.
		"""
		
		self.hidden = hidden
		try:
		    self.parent = weakref.proxy(screen)
		except TypeError:
		    self.parent = screen
		self.relx = relx
		self.rely = rely
		
		self.color = color
		
		self.set_up_handlers()
		
		# To allow derived classes to set this and then call this method safely...
		try:
			self.value
		except AttributeError:
			self.value = value

		# same again
		try:
			self.name
		except:
			self.name=name
			
		self.request_width =  width 	# widgets should honour if possible
		self.request_height = height	# widgets should honour if possible

		self.max_height = max_height
		self.max_width = max_width

		self.set_size()

		self.editing = False		# Change to true during an edit
		
		self.editable = editable
		if self.parent.curses_pad.getmaxyx()[0]-1 == self.rely: self.on_last_line = True
		else: self.on_last_line = False
		
		
	def do_colors(self):
		"Returns True if the widget should try to paint in coloour."
		if curses.has_colors() and not GlobalOptions.DISABLE_ALL_COLORS:
			return True
		else:
			return False
		
	def space_available(self):
		"""The space available left on the screen, returned as rows, columns"""
		y, x = self.parent.widget_useable_space(self.rely, self.relx)
		return y,x

	def calculate_area_needed(self): 
		"""Classes should provide a function to
calculate the screen area they need, returning either y,x, or 0,0 if
they want all the screen they can.  However, do not use this to say how
big a given widget is ... use .height and .width instead"""
		return 0,0

	def set_size(self):
		"""Set the size of the object, reconciling the user's request with the space available"""
		my, mx = self.space_available()
		my = my+1
		ny, nx = self.calculate_area_needed()
		
		if ny > 0:
			if my >= ny: self.height = ny
			else: self.height = -1
		elif self.max_height:
			if self.max_height < my: self.height = self.max_height
			else: 
				self.height = self.request_height
		else: self.height = (self.request_height or my)


		if nx > 0:              # if a minimum space is specified....
			if mx >= nx:           # if max width is greater than needed space 
			    self.width = nx    # width is needed space
			else: 
			    self.width = -1    # else raise an error
		elif self.max_width:       # otherwise if a max width is speciied
			if self.max_width <= mx: 
			    self.width = self.max_width
			else: 
			    self.width = -1
		else: 
		    self.width = self.request_width or mx

		if self.height == -1 or self.width == -1:
			# Not enough space for widget
			raise Exception("Not enough space: max y and x = %s %s" % (my, mx) ) # unsafe. Need to add error here.
	def update(self):
		"""How should object display itself on the screen. Define here, but do not actually refresh the curses
		display, since this should be done as little as possible.  This base widget puts nothing on screen."""
		pass

	def display(self):
		"""Do an update of the object AND refresh the screen"""
		self.update()
		self.parent.refresh()

	def set_editable(self, value):
		if value: self._is_editable = True
		else: self._is_editable = False

	def get_editable(self):
		return(self._is_editable)

	def clear(self, usechar=' '):
		"""Blank the screen area used by this widget, ready for redrawing"""
		for y in range(self.height):
#This method is too slow
#			for x in range(self.width+1):
#				try:
#					# We are in a try loop in case the cursor is moved off the bottom right corner of the screen
#					self.parent.curses_pad.addch(self.rely+y, self.relx + x, usechar)
#				except: pass
#Use this instead
			self.parent.curses_pad.addstr(self.rely+y, self.relx, usechar * (self.width+1))

	def edit(self):
		"""Allow the user to edit the widget: ie. start handling keypresses."""
		self.editing = 1
		self._pre_edit()
		self._edit_loop()
		return self._post_edit()

	def _pre_edit(self):
		self.highlight = 1
		old_value = self.value
		self.how_exited = False

	def _edit_loop(self):
		while self.editing:
			self.display()
			self.get_and_use_key_press()

	def _post_edit(self):
		self.highlight = 0
		self.update()
		


	def try_adjust_widgets(self):
		if hasattr(self.parent, "adjust_widgets"):
			self.parent.adjust_widgets()
	
	def try_while_waiting(self):
		if hasattr(self.parent, "while_waiting"):
			self.parent.while_waiting()

	def get_and_use_key_press(self):
			curses.meta(1)
			self.parent.curses_pad.keypad(1)
			if self.parent.keypress_timeout:
				curses.halfdelay(self.parent.keypress_timeout)
				ch = self.parent.curses_pad.getch()
				if ch == -1:
					return self.try_while_waiting()
			else:
			    self.parent.curses_pad.timeout(-1)
			    ch = self.parent.curses_pad.getch()
			# handle escape-prefixed rubbish.
			if ch == curses.ascii.ESC:
				#self.parent.curses_pad.timeout(1)
				self.parent.curses_pad.nodelay(1)
				ch2 = self.parent.curses_pad.getch()
				if ch2 != -1: 
					ch = curses.ascii.alt(ch2)
				self.parent.curses_pad.timeout(-1) # back to blocking mode
				#curses.flushinp()
			
			self.handle_input(ch)
			self.try_adjust_widgets()


	def safe_string(self, string):
		"""Check that what you are trying to display contains only
		printable chars.  (Try to catch dodgy input).  Give it a string,
		and it will return a string safe to print - without touching
		the original"""
		if string == None: return ""
		else:
			rtn = filter(self.safe_filter, string)
			return rtn
	
	def safe_filter(self, char):
		if curses.ascii.isprint(char) is True:
			return char
		else: return None


def simpletest(scr):
	import screen_area as sa
	a = sa.ScreenArea()
	b = Widget(a)


if __name__ == "__main__":
	curses.wrapper(simpletest)
	print "The circle is now complete"
