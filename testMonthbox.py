#!/bin/env python
import npyscreen

class MainFm(npyscreen.Form):
    def create(self):
        self.mb = self.add(npyscreen.MonthBox,
                    use_datetime = True)


class TestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainFm)


if __name__ == "__main__":
    A = TestApp()
    A.run()
