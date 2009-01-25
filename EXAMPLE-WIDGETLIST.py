#!/usr/bin/env python
import npyscreen
#npyscreen.disableColor()
class ActionFormExample(npyscreen.ActionForm):
	initialWidgets = [
		(npyscreen.TitleText,      {'w_id': 'TextLine', 'name': "Text:"}),
		(npyscreen.TitleFilename,  {'name' : "Filename:"}),
		(npyscreen.TitleFilename,  {'name' : "Filename:"}),
		(npyscreen.TitleDateCombo, {'name' : "Date:"}),
		(npyscreen.TitleSlider,    {'out_of': 12, 'name' : "Slider"}),
		(npyscreen.MultiLineEdit,  {'value' : """try typing here!\nMutiline text, press ^R to reformat.\n""", 'max_height': 5,})
	]

class TestApp(npyscreen.NPSApp):
	def main(self):
		# These lines create the form and populate it with widgets.
		# A fairly complex screen in only 8 or so lines of code - a line for each control.
		F = ActionFormExample(name = "Welcome to Npyscreen",)
	   #t = F.add(npyscreen.TitleText, name = "Text:", )
	   #fn = F.add(npyscreen.TitleFilename, name = "Filename:")
	   #dt = F.add(npyscreen.TitleDateCombo, name = "Date:")
	   #s = F.add(npyscreen.TitleSlider, out_of=12, name = "Slider")
	   #ml= F.add(npyscreen.MultiLineEdit, 
	   #	value = """try typing here!\nMutiline text, press ^R to reformat.\n""", 
	   #	max_height=5, rely=9)
	   #ms= F.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Pick One", 
	   #		values = ["Option1","Option2","Option3"], scroll_exit=True)
	   #ms2= F.add(npyscreen.TitleMultiSelect, max_height=4, value = [1,], name="Pick Several", 
	   #		values = ["Option1","Option2","Option3"], scroll_exit=True)
	   #
		# This lets the user play with the Form.
		F.edit()
		return F.get_widget('TextLine').value

if __name__ == "__main__":
	App = TestApp()
	print App.run()
