#!/usr/bin/python
import copy
import widget
import textbox
import curses
import titlefield

MORE_LABEL = "- more -" # string to tell user there are more options

class MultiLine(widget.Widget):
	"""Display a list of items to the user.  By overloading the display_value method, this widget can be made to 
display different kinds of objects."""
	_contained_widgets = textbox.Textfield
	def __init__(self, screen, values = None, value = None,
			slow_scroll=False, scroll_exit=False, 
			return_exit=False,
			exit_left  = False,
			exit_right = False,
		     **keywords):
		
		self.exit_left       = exit_left
		self.exit_right      = exit_right
		super(MultiLine, self).__init__(screen, **keywords)

		self.value = value
		
		# does pushing return select and then leave the widget?
		self.return_exit = return_exit
		
		
		self.slow_scroll     = slow_scroll
		self.scroll_exit     = scroll_exit
		
		self.start_display_at = 0
		self.cursor_line = 0
		self.values = values or []
		
		
		#These are just to do some optimisation tricks
		self._last_start_display_at = None
		self._last_cursor_line = None
		self._last_values = copy.copy(values)
		self._last_value = copy.copy(value)

		#override - it looks nicer.
		if self.scroll_exit: self.slow_scroll=True
		
		self._my_widgets = []
		for h in range(self.height):
			self._my_widgets.append(self._contained_widgets(screen, rely=h+self.rely, relx = self.relx))
			

	def display_value(self, vl):
		"""Overload this function to change how values are displayed.  
Should accept one argument (the object to be represented), and return a string."""
		return str(vl)

	def calculate_area_needed(self):
		return 0,0
		

	def update(self, clear=True):
		if self.hidden:
			self.clear()
			return False
		# clear = None is a good value for this widget
		display_length = len(self._my_widgets)

		if self.editing:
			if self.cursor_line < 0: self.cursor_line = 0
			if self.cursor_line > len(self.values)-1: self.cursor_line = len(self.values)-1
			
			if self.slow_scroll:
				if self.cursor_line > self.start_display_at+display_length-1:
					self.start_display_at = self.cursor_line - (display_length-1) 

				if self.cursor_line < self.start_display_at:
					self.start_display_at = self.cursor_line
			
			else:
				if self.cursor_line > self.start_display_at+(display_length-1):
					self.start_display_at = self.cursor_line

				if self.cursor_line < self.start_display_at:
					self.start_display_at = self.cursor_line - (display_length-2)
					if self.start_display_at < 0: self.start_display_at=0
		
		# What this next bit does is to not bother updating the screen if nothing has changed.
		if ( self._last_value is self.value) and \
			(self.values == self._last_values) and \
			(self.start_display_at == self._last_start_display_at) and \
			(clear != True) and \
			(self._last_cursor_line == self.cursor_line) and \
			self.editing:
				pass
			
		else:
			if clear is True: 
				self.clear()

			if (self._last_start_display_at != self.start_display_at) \
					and clear is None:
				self.clear()
			else:
				pass

			self._last_start_display_at = self.start_display_at
				

			indexer = 0 + self.start_display_at
			for line in self._my_widgets[:-1]:
				self._print_line(line, indexer)
				line.task = "PRINTLINE"
				line.update(clear=False)
				indexer += 1
			
			# Now do the final line
			line = self._my_widgets[-1]
				
			if len(self.values) <= indexer+1:
				self._print_line(line, indexer)
				line.task="PRINTLINE"
				line.update(clear=False)
			else:
				line.value = MORE_LABEL
				line.name = MORE_LABEL
				line.task = MORE_LABEL
				#line.highlight = False
				#line.show_bold = False
				line.clear()
				if self.do_colors():
					self.parent.curses_pad.addstr(self.rely+self.height-1, self.relx, MORE_LABEL, self.parent.theme_manager.findPair(self, 'CONTROL'))
				else:
					self.parent.curses_pad.addstr(self.rely+self.height-1, self.relx, MORE_LABEL)
			
			if self.editing: 
				self._my_widgets[(self.cursor_line-self.start_display_at)].highlight=True
				self._my_widgets[(self.cursor_line-self.start_display_at)].update(clear=True)


		self._last_start_display_at = self.start_display_at
		self._last_cursor_line = self.cursor_line
		self._last_values = copy.copy(self.values)
		self._last_value  = copy.copy(self.value)
		


	def _print_line(self, line, value_indexer):
			try:
				line.value = self.display_value(self.values[value_indexer])
				line.hide = False
			except IndexError:
				line.value = None
				line.show_bold=False
				line.name = None
				line.hide = True
		
			if (value_indexer == self.value) and \
				(self.value is not None):
				line.show_bold=True
			else: line.show_bold=False
		
			line.highlight=False
			
	
	def set_up_handlers(self):
		super(MultiLine, self).set_up_handlers()
		self.handlers.update ( {
					curses.KEY_UP:		self.h_cursor_line_up,
					ord('k'):		self.h_cursor_line_up,
					curses.KEY_LEFT:	self.h_cursor_line_up,
					curses.KEY_DOWN:	self.h_cursor_line_down,
					ord('j'):		self.h_cursor_line_down,
					curses.KEY_RIGHT:	self.h_cursor_line_down,
					curses.KEY_NPAGE:	self.h_cursor_page_down,
					curses.KEY_PPAGE:	self.h_cursor_page_up,
					curses.ascii.TAB:	self.h_exit_down,
					curses.ascii.NL:	self.h_select_exit,
					curses.KEY_HOME:	self.h_cursor_beginning,
					curses.KEY_END:		self.h_cursor_end,
					ord('x'):		self.h_select,
					curses.ascii.SP:	self.h_select,
					curses.ascii.ESC:	self.h_exit,
				} )
				
		if self.exit_left:
			self.handlers.update({
					curses.KEY_LEFT:	self.h_exit_left
			})
		
		if self.exit_right:
			self.handlers.update({
					curses.KEY_RIGHT:	self.h_exit_right
			})

		self.complex_handlers = [
					(self.t_input_isprint, self.h_find_char)
					]
	
	def h_find_char(self, input):
		# The following ought to work, but there is a curses keyname bug
		# searchingfor = curses.keyname(input).upper()
		# do this instead:
		searchingfor = chr(input).upper()
		for counter in xrange(len(self.values)):
			try:
				if self.values[counter].find(searchingfor) is not -1:
					self.cursor_line = counter
					break
			except AttributeError:
				break

	def t_input_isprint(self, input):
		if curses.ascii.isprint(input): return True
		else: return False
	
	
	def h_cursor_beginning(self, ch):
		self.cursor_line = 0
	
	def h_cursor_end(self, ch):
		self.cursor_line= len(self.values)

	def h_cursor_page_down(self, ch):
		self.cursor_line += (len(self._my_widgets)-1) # -1 because of the -more-
		self.start_display_at += (len(self._my_widgets)-1)
		if self.start_display_at > len(self.values) - (len(self._my_widgets)-1):
			self.start_display_at = len(self.values) - (len(self._my_widgets)-1)
	
	def h_cursor_page_up(self, ch):
		self.cursor_line -= (len(self._my_widgets)-1)
		self.start_display_at -= (len(self._my_widgets)-1)
		if self.start_display_at < 0: self.start_display_at = 0
					
	def h_cursor_line_up(self, ch):
		self.cursor_line -= 1
		if self.cursor_line < 0 and self.scroll_exit:
			self.cursor_line = 0
			self.h_exit_up(ch)

	def h_cursor_line_down(self, ch):
		self.cursor_line += 1
		if self.cursor_line >= len(self.values):
			if self.scroll_exit: 
				self.cursor_line = len(self.values)-1
				self.h_exit_down(ch)
				return True
			else: 
				self.cursor_line -=1
				return True

		if self._my_widgets[self.cursor_line-self.start_display_at].task == MORE_LABEL: 
			if self.slow_scroll:
				self.start_display_at += 1
			else:
				self.start_display_at = self.cursor_line
		
	def h_exit(self, ch):
		self.editing = False
		self.how_exited = True
	
	def h_select(self, ch):
		self.value = self.cursor_line

	def h_select_exit(self, ch):
		self.value = self.cursor_line
		if self.return_exit:
			self.editing = False
			self.how_exited=True


	def edit(self):
		self.editing = True
		self.how_exited = None
		#if self.value: self.cursor_line = self.value
		self.display()
		while self.editing:
			self.get_and_use_key_press()
			self.update(clear=None)
##			self.clear()
##			self.update(clear=False)
			self.parent.refresh()
##			curses.napms(10)
##			curses.flushinp()

class Pager(MultiLine):
	def update(self, clear=True):
		#we look this up a lot. Let's have it here.
		display_length = len(self._my_widgets)
	
		if self.start_display_at > len(self.values) - display_length: 
			self.start_display_at = len(self.values) - display_length
		if self.start_display_at < 0: self.start_display_at = 0
		
		indexer = 0 + self.start_display_at
		for line in self._my_widgets[:-1]: 
			self._print_line(line, indexer)
			indexer += 1
		
		# Now do the final line
		line = self._my_widgets[-1]
			
		if len(self.values) <= indexer+1:
			self._print_line(line, indexer)
		else:
			line.value = MORE_LABEL
			line.highlight = False
			line.show_bold = False
		
		for w in self._my_widgets: 
			# call update to avoid needless refreshes
			w.update(clear=True)
			
	def edit(self):
		# Make sure a value never gets set.
		value = self.value
		super(Pager, self).edit()
		self.value = value
	
	def h_scroll_line_up(self, input):
		self.start_display_at -= 1

	def h_scroll_line_down(self, input):
		self.start_display_at += 1	

	def h_scroll_page_down(self, input):
		self.start_display_at += len(self._my_widgets)

	def h_scroll_page_up(self, input):
		self.start_display_at -= len(self._my_widgets)

	def h_show_beginning(self, input):
		self.start_display_at = 0	
	
	def h_show_end(self, input):
		self.start_display_at = len(self.values) - len(self._my_widgets)
	
	def h_select_exit(self, input):
		self.exit(self, input)
	
	def set_up_handlers(self):
		super(Pager, self).set_up_handlers()
		self.handlers = {
					curses.KEY_UP:		self.h_scroll_line_up,
					curses.KEY_LEFT:	self.h_scroll_line_up,
					curses.KEY_DOWN:	self.h_scroll_line_down,
					curses.KEY_RIGHT:	self.h_scroll_line_down,
					curses.KEY_NPAGE:	self.h_scroll_page_down,
					curses.KEY_PPAGE:	self.h_scroll_page_up,
					curses.KEY_HOME:	self.h_show_beginning,
					curses.KEY_END:		self.h_show_end,
					curses.ascii.NL:	self.h_exit,
					curses.ascii.SP:	self.h_exit,
					ord('x'):		self.h_exit,
					ord('q'):		self.h_exit,
					curses.ascii.ESC:	self.h_exit,
				}

		self.complex_handlers = [
					]

class TitleMultiLine(titlefield.TitleText):
	_entry_type = MultiLine

	def get_values(self):
		try:
			return self.entry_widget.values
		except:
			try:
				return self.__tmp_values
			except:
				return None
	
	def set_values(self, values):
		try:
			self.entry_widget.values = values
		except:
			# probably trying to set the value before the textarea is initialised
			self.__tmp_values = values

	def del_values(self):
		del self.entry_widget.values
	
	values = property(get_values, set_values, del_values)


def testme(sa):
	import screen_area
	import Form
	#SA = screen_area.ScreenArea()
	SA = Form.Form()
	w = MultiLine(SA, 
		#relx=5, 
		#rely=2, 
		values=['test1','test2','test3', 'test4','test5','test6'], 
		#max_height=5, 
		slow_scroll=True, scroll_exit=True)
	SA.display()
	w.edit()
	w.display()
	curses.napms(2000)
	w.clear(usechar='*')
	SA.refresh()
	curses.beep()
	curses.napms(2000)
	return "%s %s" % (str(w.height),  str(w.width))

if __name__ == '__main__':
	import curses.wrapper
	print curses.wrapper(testme)
	print "No, I'll never join you"
