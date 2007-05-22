#!/usr/bin/python
import curses
import curses.ascii
import curses.wrapper
import widget

class Textfield(widget.Widget):
	def __init__(self, screen, value=None, **keywords):
		try:
			self.value
		except:
			self.value = value or ""
		
		super(Textfield, self).__init__(screen, **keywords)

		self.cursor_position = None
		
		self.show_bold = False
		self.highlight = False
		
		self.begin_at = 0	# Where does the display string begin?
		if self.parent.curses_pad.getmaxyx()[0]-1 == self.rely: self.on_last_line = True
		else: self.on_last_line = False
		
		if self.on_last_line:
			self.maximum_string_length = self.width - 1
		else:   
			self.maximum_string_length = self.width

		self.update()
		

	def calculate_area_needed(self):
		"Need one line of screen, and any width going"
		return 1,0

	
	def update(self, clear=True, cursor=True):
		"""Update the contents of the textbox, without calling the final refresh to the screen"""
		# cursor not working. See later for a fake cursor
		#if self.editing: pmfuncs.show_cursor()
		#else: pmfuncs.hide_cursor()
		
		# Not needed here -- gets called too much!
		#pmfuncs.hide_cursor()

		if clear: self.clear()

		if self.begin_at < 0: self.begin_at = 0

		if self.editing:
			if cursor:
				if self.cursor_position is False:
					self.cursor_position = len(self.value)

				elif self.cursor_position > len(self.value):
					self.cursor_position = len(self.value)

				elif self.cursor_position < 0:
					self.cursor_position = 0

				if self.cursor_position < self.begin_at:
					self.begin_at = self.cursor_position

				while self.cursor_position > self.begin_at + self.maximum_string_length: # -1:
					self.begin_at += 1
			else:
				self.parent.curses_pad.bkgdset(' ',curses.A_STANDOUT)
	
		


		if self.highlight:
			self.parent.curses_pad.bkgdset(' ',curses.A_STANDOUT)

		if self.show_bold:
			self.parent.curses_pad.attron(curses.A_BOLD)
		
		
		self._print()

		# reset everything to normal
		self.parent.curses_pad.attroff(curses.A_BOLD)
		self.parent.curses_pad.bkgdset(' ',curses.A_NORMAL)
		
		if self.editing and cursor:
			# Cursors do not seem to work on pads.
			#self.parent_screen.move(self.rely, self.cursor_position - self.begin_at)
			# let's have a fake cursor
			_cur_loc_x = self.cursor_position - self.begin_at + self.relx
			char_under_cur = self.parent.curses_pad.inch(self.rely, _cur_loc_x)
			self.parent.curses_pad.addch(self.rely, self.cursor_position - self.begin_at + self.relx, char_under_cur, curses.A_STANDOUT)

	def _print(self):
		string_to_print = self.safe_string(self.value)
		if self.value == None: return
		if self.do_colors():
			self.parent.curses_pad.addstr(self.rely,self.relx, string_to_print[self.begin_at:self.maximum_string_length+self.begin_at], 
											self.parent.theme_manager.findPair(self))
		else:
		    self.parent.curses_pad.addstr(self.rely,self.relx, string_to_print[self.begin_at:self.maximum_string_length+self.begin_at])
		    

##use addch to let us write to last corner
# This doesn't work.
#			tmpx = self.relx
#			self.parent.curses_pad.scrollok(False)
#			for c in self.value:
#				self.parent.curses_pad.addch(self.rely,tmpx, c)
#				tmpx +=1
				



	def show_brief_message(self, message):
		curses.beep()
		keep_for_a_moment = self.value
		self.value = message
		self.editing=False
		self.display()
		curses.napms(1200)
		self.editing=True
		self.value = keep_for_a_moment
		

	def edit(self):
		self.editing = 1
		self.cursor_position = len(self.value)
		self.parent.curses_pad.keypad(1)
		
		self.old_value = self.value
		
		self.how_exited = False

		while self.editing:
			self.display()
			self.get_and_use_key_press()

		self.begin_at = 0
		self.display()

		return self.how_exited, self.value

	###########################################################################################
	# Handlers and methods

	def set_up_handlers(self):
		super(Textfield, self).set_up_handlers()	
	
		# For OS X
		del_key = curses.ascii.alt('~')
		
		self.handlers.update({curses.KEY_LEFT:    self.h_cursor_left,
	                       curses.KEY_RIGHT:   self.h_cursor_right,
			       curses.KEY_DC:	   self.h_delete_right,
			       curses.ascii.DEL:   self.h_delete_left,
			       curses.ascii.BS:    self.h_delete_left,
			       curses.KEY_BACKSPACE: self.h_delete_left,
			       # mac os x curses reports DEL as escape oddly
			       # no solution yet			       
			       "^K":		   self.h_erase_right,
			       "^U":		   self.h_erase_left,
			})

		self.complex_handlers.extend((
                                             (self.t_input_isprint, self.h_addch),
		                            # (self.t_is_ck, self.h_erase_right),
					    # (self.t_is_cu, self.h_erase_left),
					    ))

	def t_input_isprint(self, input):
		if curses.ascii.isprint(input) and \
		(chr(input) not in '\n\t\r'): 
			return True
		
		else: return False

	def h_addch(self, input):
		if self.editable:
			#self.value = self.value[:self.cursor_position] + curses.keyname(input) \
			#	+ self.value[self.cursor_position:]
			#self.cursor_position += len(curses.keyname(input))
			
			# workaround for the metamode bug:
			self.value = self.value[:self.cursor_position] + chr(input) \
				+ self.value[self.cursor_position:]
			self.cursor_position += len(chr(input))

			# or avoid it entirely:
			#self.value = self.value[:self.cursor_position] + curses.ascii.unctrl(input) \
			#	+ self.value[self.cursor_position:]
			#self.cursor_position += len(curses.ascii.unctrl(input))

	def h_cursor_left(self, input):
		self.cursor_position -= 1

	def h_cursor_right(self, input):
		self.cursor_position += 1

	def h_delete_left(self, input):
		if self.editable and self.cursor_position > 0:
			self.value = self.value[:self.cursor_position-1] + self.value[self.cursor_position:]
		
		self.cursor_position -= 1
		self.begin_at -= 1

	
	def h_delete_right(self, input):
		if self.editable:
			self.value = self.value[:self.cursor_position] + self.value[self.cursor_position+1:]

	def h_erase_left(self, input):
		if self.editable:
			self.value = self.value[self.cursor_position:]
			self.cursor_position=0
	
	def h_erase_right(self, input):
		if self.editable:
			self.value = self.value[:self.cursor_position]
			self.cursor_postition = len(self.value)
			self.begin_at = 0
	
class FixedText(Textfield):
	def h_delete_right(self, *args):
		pass
	def h_erase_right(self, *args):
		pass
	def h_delete_left(self, *args):
		pass
	def h_erase_left(self, *args):
		pass
	def h_addch(self,*args):
		pass
	def h_cursor_left(self, input):
		if self.begin_at > 0:
			self.begin_at -= 1

	def h_cursor_right(self, input):
		if len(self.value) - self.begin_at > self.maximum_string_length:
			self.begin_at += 1

	def update(self, clear=True,):
		super(FixedText, self).update(clear=clear, cursor=False)
	
	def edit(self):
		self.editing = 1
		self.highlight = False
		self.cursor_position = 0
		self.parent.curses_pad.keypad(1)
		
		self.old_value = self.value
		
		self.how_exited = False

		while self.editing:
			self.display()
			self.get_and_use_key_press()

		self.begin_at = 0
		self.highlight = False
		self.display()

		return self.how_exited, self.value

def cleartest(screen):
	import screen_area
	SA = screen_area.ScreenArea()
	w  = Textfield(SA, rely=1, relx=3)
	w.value = "This is some text! height: %s, width %s" % (w.height, w.width)
	w.display()
	curses.napms(1000)
	curses.beep()
	w.clear()
	SA.refresh()
	curses.napms(2000)
	
def simpletest(screen):
	import screen_area
	SA = screen_area.ScreenArea()
	w = Textfield(SA, rely=23, relx=66)
	w.value = "height: %s, width %s" % (w.height, w.width)
	w.edit()
	w.update()
	SA.refresh()
	curses.napms(2000)
	

if __name__ == "__main__":
	curses.wrapper(cleartest)
	print "The circle is now complete"
