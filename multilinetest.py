import npyscreen

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm("MAIN", MainForm(lines=47))

class MainForm(npyscreen.Form):
    def create(self):
        vl = []
        for x in range(100):
            vl.append("Value %s" % x)
        self.add(npyscreen.MultiSelect, values=vl)

def main():
    TA = MyTestApp()
    TA.run()


if __name__ == '__main__':
    main()
