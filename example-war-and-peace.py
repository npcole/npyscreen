#!/usr/bin/env python
import npyscreen

class EditorFormExample(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = npyscreen.MultiLineEdit

class TestApp(npyscreen.NPSApp):
    def main(self):
        F = EditorFormExample()
        F.wStatus1.value = "Status Line "
        F.wStatus2.value = "Second Status Line "
        with open("/Users/nicholas/Downloads/pg2600.txt", 'r') as war_and_peace:
             text = war_and_peace.read()
        F.wMain.value = text        


        F.edit()


if __name__ == "__main__":
    App = TestApp()
    App.run()
