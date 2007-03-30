#!/usr/bin/env python
import npyscreen

class TestApp(npyscreen.NPSApp):
	def main(self):
		# These lines create the form and populate it with widgets.
		# A fairly complex screen in only 8 or so lines of code - a line for each control.
		F = npyscreen.ActionForm(name = "Welcome to Npyscreen",)
		t = F.add(npyscreen.TitleText, name = "Text:", )
		fn = F.add(npyscreen.TitleFilename, name = "Filename:")
		dt = F.add(npyscreen.TitleDateCombo, name = "Date:")
		s = F.add(npyscreen.TitleSlider, out_of=12, name = "Slider")
		ml= F.add(npyscreen.MultiLineEdit, 
			value = """try typing here! Mutiline text, press ^R to reformat.\nPress ^X for automatically created list of menus""", 
			max_height=5, rely=9)
		ms= F.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Pick One", 
				values = ["Option1","Option2","Option3"], scroll_exit=True)
		ms2= F.add(npyscreen.TitleMultiSelect, max_height=4, value = [1,], name="Pick Several", 
				values = ["Option1","Option2","Option3"], scroll_exit=True)
		
		# This block of code adds a popup menu with lots of options.
		mnu = F.add_menu(name="Nothing Menu", key="^F")
		mnu.add_item("Do Nothing",   self.tstDoNothing)
		mnu.add_item("Do Nothing 2", self.tstDoNothing)
		mnu.add_item("Do Nothing 3", self.tstDoNothing)
		for x in range(10): # Just add lots so we can show off what happens with a long menu.
			mnu.add_item("Do Nothing x", self.tstDoNothing)
		
		# This lets the user play with the Form.
		F.edit()
		

	def tstDoNothing(self):
		import curses
		curses.beep()

if __name__ == "__main__":
	App = TestApp()
	App.run()
