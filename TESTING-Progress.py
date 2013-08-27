import npyscreen


class ProcessBar(npyscreen.Slider):
    def __init__(self, *args, **keywords):
        super(ProcessBar, self).__init__(*args, **keywords)
        self.editable = False
        
class ProcessBarBox(npyscreen.BoxTitle):          
    _contained_widget = ProcessBar



class TestApp(npyscreen.NPSApp):
    def main(self):
        F = npyscreen.Form(name = "Welcome to Npyscreen",)
        s = F.add(ProcessBarBox, max_height=3, out_of=12, value=5, name = "Text:")
        
        #s.editable=False


        # This lets the user play with the Form.
        F.edit()


if __name__ == "__main__":
    App = TestApp()
    App.run()   
