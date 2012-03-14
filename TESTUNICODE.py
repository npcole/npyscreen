#!/usr/bin/env python
# encoding: utf-8

import npyscreen
#npyscreen.disableColor()
class TestApp(npyscreen.NPSApp):
    def main(self):
        # These lines create the form and populate it with widgets.
        # A fairly complex screen in only 8 or so lines of code - a line for each control.
        F = npyscreen.Form(name = "Welcome to Npyscreen",)
        t = F.add(npyscreen.TextfieldUnicode, name = "Text:", value='Ω—Ƣ' )
        t.left_margin=10
        a = F.add(npyscreen.Textfield, name = "Text:", value='This is the original textfield' )
        # This lets the user play with the Form.
        F.edit()


if __name__ == "__main__":
    App = TestApp()
    App.run()   
