import npyscreen

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addFormClass("MAIN", MainForm)

class MainForm(npyscreen.FileSelector):
    pass

def main():
    TA = MyTestApp()
    TA.run()


if __name__ == '__main__':
    main()
