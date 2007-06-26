#!/usr/bin/env python
import npyscreen
import time
import curses

class TimeoutApplication(npyscreen.NPSAppManaged):
	def onStart(self):
		self.mainForm = self.addForm('MAIN', TimeoutForm)
		
		
class TimeoutForm(npyscreen.Form):
	def create(self):
		self.keypress_timeout = 10
		self.timeWidget       = self.add(npyscreen.TitleText, name="Time:", value=None, editable = None)
	
	def afterEditing(self):
		self.parentApp.NEXT_ACTIVE_FORM = None
	
	def while_waiting(self):
		self.timeWidget.value = time.asctime()
		self.timeWidget.display()


if __name__ == "__main__":
	app = TimeoutApplication()
	app.run()