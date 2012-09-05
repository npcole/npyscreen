#! /usr/bin/env python3

import sys
import npyscreen

class TestMenuForm(npyscreen.FormBaseNew):
    def create(self):
        self.Selection = self.add(npyscreen.TitleMultiSelect,
                                  name="select",
                                  values=["a","b","c"],
                                  max_height=3,
                                  scroll_exit=True)
        self.messageBox = self.add(npyscreen.Pager,
                                   name="Messages",
                                   max_height=4,
                                   editable=False)
    def while_editing(self,arg):
        if arg is self.Selection:
            if len(arg.value) == 0:
                self.messageBox.values = ["please select at least one",
                                          arg.value,
                                          len(arg.value)]
            else:
                self.messageBox.values = [repr(arg.value),
                                          arg.value,
                                          len(arg.value)]
            self.messageBox.display()
            npyscreen.notify_yes_no('Has this worked', editw=1)
        
class TestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        testMenuForm = TestMenuForm(name="Selection")
        self.registerForm('MAIN', testMenuForm)


def main(args):
    App = TestApp()
    App.run()

if __name__ == '__main__':
    main(sys.argv)

