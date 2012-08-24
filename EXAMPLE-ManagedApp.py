#!/usr/bin/env python
# encoding: utf-8
"""
ExampleManaged.py

Created by Nicholas Cole on 2007-02-22.
"""

import npyscreen, curses

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm("MAIN", MainForm())
    
class MainForm(npyscreen.Form):
    def create(self):
        self.add(npyscreen.TitleText, name = "Text:", value= "Press Escape to quit application" )
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE]  = self.exit_application    

    def exit_application(self):
        curses.beep()
        self.parentApp.setNextForm(None)
        self.editing = False

def main():
    TA = MyTestApp()
    TA.run()


if __name__ == '__main__':
    main()

