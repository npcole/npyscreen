#!/usr/bin/env python
import npyscreen

class TestApp(npyscreen.NPSApp):
    def main(self):
        F = npyscreen.FormMutt()
        F.add
        F.wStatus1.value = "Status Line "
        F.wStatus2.value = "Second Status Line "
        F.wMain.values   = [str(x) for x in range(500)]
        
        F.edit()


if __name__ == "__main__":
    App = TestApp()
    App.run()
