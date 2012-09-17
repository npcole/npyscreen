#!/usr/bin/env python
# encoding: utf-8

import npyscreen, curses

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm("MAIN", MainForm())

class MainForm(npyscreen.FormWithMenus):
    def create(self):
        self.add(npyscreen.TitleText, name = "Text:", value= "Press Escape to quit application" )
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE]  = self.exit_application    
        
        # The menus are created here.
        self.m1 = self.add_menu(name="Main Menu")
        self.m1.addItemsFromList([
            ("Just Beep",   self.whenJustBeep),
            ("Exit Application", self.exit_application),
        ])
        
        self.m2 = self.add_menu(name="Another Menu")
        self.m2.addItemsFromList([
            ("Just Beep",   self.whenJustBeep),
        ])
        
        self.m3 = self.m2.addNewSubmenu("A sub menu")
        self.m3.addItemsFromList([
            ("Just Beep",   self.whenJustBeep),
        ])        

    def whenJustBeep(self):
        curses.beep()

    def exit_application(self):
        curses.beep()
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()

def main():
    TA = MyTestApp()
    TA.run()


if __name__ == '__main__':
    main()

