#!/usr/bin/env python
# encoding: utf-8

import npyscreen
#npyscreen.disableColor()
class TestApp(npyscreen.NPSApp):
    def main(self):
        # These lines create the form and populate it with widgets.
        # A fairly complex screen in only 8 or so lines of code - a line for each control.
        F = npyscreen.Form(name = "Welcome to Npyscreen",)
        t = F.add(npyscreen.BoxBasic, name = "Basic Box:", max_width=60, max_height=3)
        t.footer = "This is a footer"
        
        t2 = F.add(npyscreen.BoxTitle, name="Box Title:", max_height=6)
        t2.entry_widget.scroll_exit = True
        t2.values = ["Hello", 
            "This is a Test", 
            "This is another test", 
            "And here is another line",
            "And one more."]
        
        F.edit()
        
        
if __name__ == "__main__":
    App = TestApp()
    App.run()   
