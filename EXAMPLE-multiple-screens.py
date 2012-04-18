import npyscreen, curses

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="Screen 1", color="IMPORTANT",)
        self.addForm("SECOND", MainForm, name="Screen 2", color="WARNING",)
    
    def change_form(self, name):
        self.switchForm(name)
    
    def onExit(self):
        print("Goodbye!")
    
class MainForm(npyscreen.ActionForm):
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
    
    def on_ok(self):
        self.parentApp.switchForm(None)
    

def main():
    TA = MyTestApp()
    TA.run()


if __name__ == '__main__':
    main()
