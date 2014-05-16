#!/usr/bin/env python
import npyscreen

class TestForm(npyscreen.FormMutt):
    def __init__(self, *args, **keywords):
        super(TestForm, self).__init__(*args, **keywords)
        self.add_handlers({"^R": self.go_to_main})
    
    def go_to_main(self, t):
        raise ValueError



class TestApp(npyscreen.NPSApp):
    def main(self):
        F = TestForm()
        F.wStatus1.value = "Status Line "
        F.wStatus2.value = "Second Status Line "
        F.wMain.values   = [str(x) for x in range(500)]
        
        F.edit()


if __name__ == "__main__":
    App = TestApp()
    App.run()
