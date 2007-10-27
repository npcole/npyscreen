#!/usr/bin/python
import screen_area
import widget
import button
import curses.wrapper
import weakref
import pmfuncs
#import Menu
import GlobalOptions




class Form(screen_area.ScreenArea, widget.InputHandler):
	OK_BUTTON_BR_OFFSET = (2,6)
	OKBUTTON_TYPE = button.MiniButton
	DEFAULT_X_OFFSET = 2
	def __init__(self, name=None, framed=True, help=None, color='FORMDEFAULT', *args, **keywords):
		super(Form, self).__init__(*args, **keywords)
		self.framed = framed
		self.name=name
		self.editing = False
		self._widgets__= []
		## OLD MENU CODE REMOVED self.__menus  = []

		self.nextrely = 2
		self.nextrelx = self.__class__.DEFAULT_X_OFFSET
		self.editw = 0 # Index of widget to edit.

		self.help = help
		
		self.color = color
		

		self.set_up_handlers()
		self.set_up_exit_condition_handlers()

		self.create()

	def adjust_widgets(self):
		"""This method can be overloaded by derived classes. It is called when editing any widget, as opposed to
		the while_editing() method, which may only be called when moving between widgets.  Since it is called for
		every keypress, and perhaps more, be careful when selecting what should be done here."""

	def create(self):
		"""Programmers should over-ride this in derived classes, creating widgets here"""
		pass
	
	def set_up_handlers(self):
		self.complex_handlers = []
		self.handlers = { 
					curses.KEY_F1: self.h_display_help,
					"KEY_F(1)": self.h_display_help,
					"!h":	    self.h_display_help,
					"^L":	    self.h_display,
					#curses.KEY_RESIZE:	self.h_display,
					}

	def set_up_exit_condition_handlers(self):
		# What happens when widgets exit?
		# each widget will set it's how_exited value: this should
		# be used to look up the following table.
		
		self.how_exited_handers = {
			widget.EXITED_DOWN:    self.find_next_editable,
			widget.EXITED_RIGHT:   self.find_next_editable,
			widget.EXITED_UP:      self.find_previous_editable,
			widget.EXITED_LEFT:    self.find_previous_editable,
			widget.EXITED_ESCAPE:  self.do_nothing,
			True:	               self.find_next_editable, # A default value
			widget.EXITED_MOUSE:   self.get_and_use_mouse_event,
			}

	def handle_exiting_widgets(self, condition):
		self.how_exited_handers[condition]()
		
	def do_nothing(self, *args, **keywords):
		pass

	def while_editing(self, *args, **keywords):
		"""This function gets called during the edit loop, on each iteration
		of the loop.  It does nothing: it is here to make customising the loop
		as easy as overriding this function. A proxy to the currently selected widget is 
		passed to the function."""

	def on_screen(self):
		# is the widget in editw on sreen at the moment?
		# if not, alter screen so that it is.
		
		w = weakref.proxy(self._widgets__[self.editw])
		
		max_y, max_x = self._max_physical()

		w_my, w_mx = w.calculate_area_needed()
		
		# always try to show the top of the screen.
		self.show_from_y = 0
		self.show_from_x = 0
		
		while w.rely + w_my -1 > self.show_from_y + max_y:
			self.show_from_y += 1

		while w.rely < self.show_from_y:
			self.show_from_y -= 1
			

		while w.relx + w_mx -1 > self.show_from_x + max_x:
			self.show_from_x += 1

		while w.relx < self.show_from_x:
			self.show_from_x -= 1
		
## REMOVING OLD MENU CODE  def menuOfMenus(self, *args, **keywords):
## REMOVING OLD MENU CODE  	"""DEPRICATED"""
## REMOVING OLD MENU CODE  	tmpmnu = Menu.Menu(name = "All Menus", show_aty=2, show_atx=2)
## REMOVING OLD MENU CODE  	#tmpmnu.before_item_select = self.display
## REMOVING OLD MENU CODE  	for mnu in self.__menus:
## REMOVING OLD MENU CODE  		text = ""
## REMOVING OLD MENU CODE  		if mnu.name: text += mnu.name
## REMOVING OLD MENU CODE  		for keypress in self.handlers.keys():
## REMOVING OLD MENU CODE  			if self.handlers[keypress] == mnu.edit:
## REMOVING OLD MENU CODE  				if keypress: text += " (%s)" % keypress
## REMOVING OLD MENU CODE  				text += " >"
## REMOVING OLD MENU CODE  		tmpmnu.add_item(text, mnu.edit)
## REMOVING OLD MENU CODE  		tmpmnu.edit()
## REMOVING OLD MENU CODE
## REMOVING OLD MENU CODE  def add_menu(self, menu=None, key=None, *args, **keywords):
## REMOVING OLD MENU CODE  	"""DEPRICATED"""
## REMOVING OLD MENU CODE  	if menu is None:
## REMOVING OLD MENU CODE  		mu = Menu.Menu(*args, **keywords)
## REMOVING OLD MENU CODE  		self.__menus.append(mu)
## REMOVING OLD MENU CODE  	else:
## REMOVING OLD MENU CODE  		mu = menu
## REMOVING OLD MENU CODE  		self.__menus.append(mu)
## REMOVING OLD MENU CODE  	self.add_handlers({key: mu.edit})
## REMOVING OLD MENU CODE  	return weakref.proxy(mu)

	def edit(self):
		"""Edit the fields until the user selects the ok button added in the lower right corner. Button will
		be removed when editing finishes"""
		self.editing=True
		if self.editw < 0: self.editw=0
		if self.editw > len(self._widgets__)-1:
			self.editw = len(self._widgets__)-1
	
		if not self._widgets__[self.editw].editable: self.find_next_editable()
		# Add ok button. Will remove later
		tmp_rely, tmp_relx = self.nextrely, self.nextrelx
		my, mx = self.curses_pad.getmaxyx()
		ok_button_text = "OK"
		my -= self.__class__.OK_BUTTON_BR_OFFSET[0]
		mx -= len(ok_button_text)+self.__class__.OK_BUTTON_BR_OFFSET[1]
		self.ok_button = self.add_widget(self.__class__.OKBUTTON_TYPE, name=ok_button_text, rely=my, relx=mx)
		ok_button_postion = len(self._widgets__)-1
		self.ok_button.update()

		self.display()

		while not self._widgets__[self.editw].editable:
			self.editw += 1
			if self.editw > len(self._widgets__)-1: 
				self.editing = False
				return False
		
		while self.editing:
			if not self.ALL_SHOWN: self.on_screen()
			self.while_editing(weakref.proxy(self._widgets__[self.editw]))
			self._widgets__[self.editw].edit()
			self._widgets__[self.editw].display()
			
			self.handle_exiting_widgets(self._widgets__[self.editw].how_exited)
			
			if self.editw > len(self._widgets__)-1: self.editw = len(self._widgets__)-1
			if self.ok_button.value:
				self.editing = False
		
		self.ok_button.destroy()
		del self._widgets__[ok_button_postion]
		del self.ok_button
		self.nextrely, self.nextrelx = tmp_rely, tmp_relx
		self.display()

		self.editing = False
			
	
	def h_display_help(self, input):
		if self.help == None: return
		if self.name:
			help_name="%s Help" %(self.name)
		else: help_name=None
		curses.flushinp()
		select.ViewText(self.help, name=help_name)
		self.display()
		return True

	def h_display(self, input):
		self.curses_pad.redrawwin()
		self.display()
		
	def get_and_use_mouse_event(self):
		curses.beep()
	
			
	def find_next_editable(self, *args):
		if not self.editw == len(self._widgets__):		
			for n in xrange(self.editw+1, len(self._widgets__)):
				if self._widgets__[n].editable and not self._widgets__[n].hidden: 
					self.editw = n
					break
		self.display()
		

	def find_previous_editable(self, *args):
		if not self.editw == 0:		
			# remember that xrange does not return the 'last' value,
			# so go to -1, not 0! (fence post error in reverse)
			for n in xrange(self.editw-1, -1, -1 ):
				if self._widgets__[n].editable and not self._widgets__[n].hidden: 
					self.editw = n
					break

	def widget_useable_space(self, rely=0, relx=0):
		#Slightly misreports space available.
		mxy, mxx = self.lines-1, self.columns-1
		return (mxy-1-rely, mxx-1-relx)

	def display(self):
		#APPLICATION_THEME_MANAGER.setTheme(self)
		if curses.has_colors() and not GlobalOptions.DISABLE_ALL_COLORS:
			color_attribute = self.theme_manager.findPair(self)
			self.curses_pad.bkgdset(' ', color_attribute)
			self.curses_pad.attron(color_attribute)
		self.curses_pad.erase()
		self.draw_form()
		for w in self._widgets__: 
			w.update(clear=False)
	
		self.refresh()

	def draw_form(self):
		if self.framed:
			self.curses_pad.border()
			
			try:
				if self.name:
					_title = self.name[:(self.columns-4)]
					self.curses_pad.addstr(0,1, ' '+str(_title)+' ')
			except:
				pass

			if self.help and self.editing:
				try:
					help_advert = " Help: F1 or M-h "
					self.curses_pad.addstr(
					 0, self.curses_pad.getmaxyx()[1]-len(help_advert)-2, help_advert 
					 )
				except:
					pass

	def add_widget(self, widgetClass, max_height=None, rely=None, relx=None, *args, **keywords):
		"""Add a widget to the form.  The form will do its best to decide on placing, unless you override it.
		The form of this function is add_widget(WidgetClass, ....) with any arguments or keywords supplied to
		the widget. The wigdet will be added to self._widgets__
		
		It is safe to use the return value of this function to keep hold of the widget, since that is a weak
		reference proxy, but it is not safe to keep hold of self._widgets__"""

		if rely is None:
			rely = self.nextrely
		if relx is None:
			relx = self.nextrelx

		if max_height is False:
			max_height = self.curses_pad.getmaxyx()[0] - rely - 1

		_w = widgetClass(self, 
				rely=rely, 
				relx=relx, 
				max_height=max_height, 
				*args, **keywords)
		
		self.nextrely = _w.height + _w.rely 
		self._widgets__.append(_w)

		return weakref.proxy(_w)
	
	def useable_space(self, rely=0, relx=0):
		"""Reports space left on physical screen. Widgets should use widget_useable_space instead."""
		mxy, mxx = curses.newwin(0,0).getmaxyx()
		return ((mxy-rely)-1, (mxx-relx)-2)
	
	add = add_widget
	
class TitleForm(Form):
	"""A form without a box, just a title line"""
	OK_BUTTON_BR_OFFSET = (1,6)
	OKBUTTON_TYPE = button.MiniButton
	DEFAULT_X_OFFSET = 1
	def draw_form(self):
		MAXY, MAXX = self.curses_pad.getmaxyx()
		self.curses_pad.hline(0, 0, curses.ACS_HLINE, MAXX)	
		try:
			if self.name:
				self.curses_pad.addstr(0,1, ' '+str(self.name)+' ')
		except:
			pass

		if self.help and self.editing:
			try:
				help_advert = " Help: F1 or M-h "
				self.curses_pad.addstr(
				 0, self.curses_pad.MAXX-len(help_advert)-2, help_advert 
				 )
			except:
				pass

class TitleFooterForm(TitleForm):
	def draw_form(self):
		MAXY, MAXX = self.curses_pad.getmaxyx()

		if self.editing:
			self.curses_pad.hline(MAXY-1, 0, curses.ACS_HLINE, 
					MAXX - self.__class__.OK_BUTTON_BR_OFFSET[1] - 1)
		else:
			self.curses_pad.hline(MAXY-1, 0, curses.ACS_HLINE, MAXX-1)

		super(TitleFooterForm, self).draw_form()

class SplitForm(Form):
	"""Just the same as the Title Form, but with a horizontal line"""
	def draw_form(self):
		MAXY, MAXX = self.curses_pad.getmaxyx()
		super(SplitForm, self).draw_form()
		self.curses_pad.hline(MAXY//2-1, 1, curses.ACS_HLINE, MAXX-2)
		
	def get_half_way(self):
		return self.curses_pad.getmaxyx()[0] // 2



def testmem(sa):
	import titlefield
	import textbox
	import slider
	import multiline
	while 1:
		F = Form(name="Testing")
		w = F.add_widget(titlefield.TitleText)
		str = "useable space = %s, %s; my height and width is: %s, %s" % (F.useable_space()[0], F.useable_space()[1], w.height, w.width)
		w.value = str
		w2 = F.add_widget(textbox.Textfield)
		str2 = "useable space = %s, %s; my height and width is: %s, %s" % (F.useable_space()[0], F.useable_space()[1], w2.height, w2.width)
		w2.value = str2
		w3 = F.add_widget(slider.Slider)
		#w4 = F.add_widget(multiline.MultiLine, height=5)
		F.display()

def testme(sa):
	import titlefield
	import textbox
	import slider
	import multiline

	F = TitleFooterForm(name="Testing")
	w = F.add_widget(titlefield.TitleText)
	str = "useable space = %s, %s; my height and width is: %s, %s" % (F.useable_space()[0], F.useable_space()[1], w.height, w.width)
	w.value = str
	w2 = F.add_widget(textbox.Textfield)
	str2 = "useable space = %s, %s; my height and width is: %s, %s" % (F.useable_space()[0], F.useable_space()[1], w2.height, w2.width)
	w2.value = str2
	w3 = F.add_widget(slider.Slider)
	#w4 = F.add_widget(multiline.MultiLine, height=5)
	F.display()
	F.edit()
	curses.napms(1500)
	

if __name__ == '__main__':
	curses.wrapper(testme)
	print "No Luke, I am your father"
