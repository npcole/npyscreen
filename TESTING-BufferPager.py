#!/usr/bin/env python
import npyscreen

class EditorFormExample(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = npyscreen.BufferPager

class TestApp(npyscreen.NPSApp):
    def main(self):
        F = EditorFormExample()
        F.wStatus1.value = "Status Line "
        F.wStatus2.value = "Second Status Line "
        F.wMain.editable  = False
        F.wMain.autowrap = False
        
        #F.wMain.buffer([str(r) for r in range(100)], scroll_if_editing=True)
        #with open("/Users/nicholas/Downloads/pg2600.txt", 'r') as war_and_peace:
        with open("setup.py", 'r') as war_and_peace:
            F.wMain.buffer(war_and_peace.readlines())
            #F.wMain.values = war_and_peace.readlines()
        
        F.edit()


if __name__ == "__main__":
    App = TestApp()
    App.run()
