import npyscreen


class TestForm(npyscreen.ActionFormV2):
    def create(self):
        self.testfield = self.add_widget(npyscreen.TitleMultiSelect,
                                         name="test label",
                                         max_height=15,
                                         rely=2,
                                         relx=2,
                                         values=["value1", "value2", "value3"])


class testapp(npyscreen.NPSAppManaged):
    # def __init__(self):
    #    super().__init__()

    def onStart(self):
        self.addForm("MAIN",
                     TestForm, "Test Form",
                     use_max_space=True)


# create the app
app = testapp()
app.run()
