#!/usr/bin/env python
# encoding: utf-8

import npyscreen
#npyscreen.disableColor()
class TestApp(npyscreen.NPSApp):
    def main(self):
        F  = npyscreen.Form(name = "Welcome to Npyscreen",)
        ms = F.add(npyscreen.Button, name="Button", max_width=7, rely = -5, relx = -13)
        ml = F.add(npyscreen.TitleMultiLine, name="Multiline", relx = -55, rely = 5, max_height=12, values = [1,2,3])
        
        F.edit()

if __name__ == "__main__":
    App = TestApp()
    App.run()   
