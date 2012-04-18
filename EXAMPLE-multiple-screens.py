import npyscreen, curses

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm("MAIN", MainForm(name="Screen 1", color="IMPORTANT"))
        self.registerForm("SECOND", MainForm(name="Screen 2", color="WARNING"))
    
    def change_form(self, name):
        self.switchForm(name)
    
class MainForm(npyscreen.Form):
    def create(self):
        self.add(npyscreen.TitleText, name = "Text:", value= "Press ^T to change screens" )
        self.add_handlers({"^T": self.change_forms})

    def change_forms(self, *args, **keywords):
        #curses.beep()
        if self.name == "Screen 1":
            change_to = "SECOND"
        else:
            change_to = "MAIN"
        self.parentApp.change_form(change_to)
        #self.editing=False
    

def main():
    TA = MyTestApp()
    TA.run()


if __name__ == '__main__':
    main()
