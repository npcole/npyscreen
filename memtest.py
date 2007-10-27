#!/usr/bin/env python
import npyscreen
import EXAMPLE

#def Mainloop(scr):
#	while 1:
#		sampleform()
#
#def sampleform():
#	F = npyscreen.Form(name = "Welcome to Npyscreen")
#	t = F.add(npyscreen.TitleText, name = "Text:")
#	p = F.add(npyscreen.TitlePassword, name = "Password:")
#	fn = F.add(npyscreen.TitleFilename, name = "Filename:")
#	s = F.add(npyscreen.TitleSlider, out_of=12, name = "Slider")
#	ml= F.add(npyscreen.MultiLineEdit, value = "try typing here! Mutiline text, press ^R to reformat.", max_height=4)
#	ms= F.add(npyscreen.MultiSelect, max_height=4, value = [1,], values = ["Option1","Option2","Option3"], scroll_exit=True)

class TestMem(npyscreen.NPSApp):
	def main(self):
		F = npyscreen.Form(name = "Welcome to Npyscreen")
		t = F.add(npyscreen.TitleText, name = "Text:")
		p = F.add(npyscreen.TitlePassword, name = "Password:")
		fn = F.add(npyscreen.TitleFilename, name = "Filename:")
		s = F.add(npyscreen.TitleSlider, out_of=12, name = "Slider")
		ml= F.add(npyscreen.MultiLineEdit, value = "try typing here! Mutiline text, press ^R to reformat.", max_height=3, rely=7)
		ms= F.add(npyscreen.MultiSelect, max_height=4, value = [1,], values = ["Option1","Option2","Option3"], scroll_exit=True)
		
		F.display()
		
if __name__ == "__main__":
	Test = TestMem()
	Test.run()
	while 1:
		Test = TestMem()
		Test.main()
	
