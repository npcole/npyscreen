import npyscreen

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm("MAIN", MainForm())

class MainForm(npyscreen.Form):
    def create(self):
        self.add(npyscreen.Textfield, color='CRITICAL', value='Testing Testing')
        self.color = "CRITICAL"
        pass

def main():
    TA = MyTestApp()
    TA.run()


if __name__ == '__main__':
    main()
