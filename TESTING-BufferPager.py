#!/usr/bin/env python
import npyscreen

class EditorFormExample(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = npyscreen.BufferPager

class TestApp(npyscreen.NPSApp):
    def main(self):
        F = EditorFormExample()
        F.wStatus1.value = "Status Line "
        F.wStatus2.value = "Second Status Line "
        
        F.wMain.buffer([str(r) for r in range(100)], scroll_if_editing=True)
        
        F.edit()


if __name__ == "__main__":
    App = TestApp()
    App.run()
