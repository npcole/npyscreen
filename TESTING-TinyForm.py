#!/usr/bin/env python
# encoding: utf-8
import npyscreen

class TinyForm(npyscreen.FormBaseNew):
    DEFAULT_NEXTRELY = 0
    BLANK_LINES_BASE   = 0

class TestApp(npyscreen.NPSApp):
    def main(self):
        F  = TinyForm(name = "Welcome to Npyscreen", 
                        framed=False, 
                        lines=1, 
                        columns=0, 
                        minimum_lines = 1)
        ms = F.add(npyscreen.TitleText, name='Test', )        
        F.edit()
if __name__ == "__main__":
    App = TestApp()
    App.run()   
