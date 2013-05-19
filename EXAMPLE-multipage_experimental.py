#!/usr/bin/env python
# encoding: utf-8

import npyscreen
#npyscreen.disableColor()
class TestApp(npyscreen.NPSApp):
    def main(self):
        # These lines create the form and populate it with widgets.
        # A fairly complex screen in only 8 or so lines of code - a line for each control.
        F = npyscreen.FormMultiPageActionWithMenus(name = "Welcome to Npyscreen",)
        t = F.add(npyscreen.TitleText, name = "Text:",)
        fn = F.add(npyscreen.TitleFilename, name = "Filename:")
        dt = F.add(npyscreen.TitleDateCombo, name = "Date:")
        s = F.add(npyscreen.TitleSlider, out_of=12, name = "Slider")
        
        # The new page is created here.
        new_page = F.add_page()
        
        ml= F.add(npyscreen.MultiLineEdit, 
            value = """try typing here!\nMutiline text, press ^R to reformat.\n""", 
                    max_height=5,)
        ms= F.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Pick One", 
                values = ["Option1","Option2","Option3"], scroll_exit=True)
        ms2= F.add(npyscreen.TitleMultiSelect, max_height =-2, value = [1,], name="Pick Several", 
                values = ["Option1","Option2","Option3"], scroll_exit=True)
        
        F.switch_page(0)
        
        def on_ok():
            npyscreen.notify_confirm("OK Button Pressed!")
        F.on_ok = on_ok
        # This lets the user play with the Form.
        F.edit()
        


if __name__ == "__main__":
    App = TestApp()
    App.run()   
