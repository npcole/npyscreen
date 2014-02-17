#!/usr/bin/env python
import npyscreen
class TestApp(npyscreen.NPSApp):
    def main(self):
        # These lines create the form and populate it with widgets.
        # A fairly complex screen in only 8 or so lines of code - a line for each control.
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        F = npyscreen.SplitForm(name = "Welcome to Npyscreen",)
        t = F.add(npyscreen.Textfield, name = "Text:", )
        t1 = F.add(npyscreen.TitleText, name = "Text:", )
        t2 = F.add(npyscreen.TitleMultiSelect, name="Testing", values=range(200))
        # This lets the user play with the Form.
        F.edit()


if __name__ == "__main__":
    App = TestApp()
    App.run()
