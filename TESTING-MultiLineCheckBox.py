#!/usr/bin/env python
# encoding: utf-8
import npyscreen
#npyscreen.disableColor()


class MultiSelectWidgetTesting(npyscreen.MultiSelect):
    _contained_widgets = npyscreen.CheckBoxMultiline
    _contained_widget_height = 2
    
    def display_value(self, vl):
        return vl



class TestApp(npyscreen.NPSApp):
    def main(self):
        value_list = [
            ["This is", "the first"],
            ["This is", "the second"],
            ["This is", "the third"],
            ["This is", "the fourth"],
        ]
        F  = npyscreen.Form(name = "Welcome to Npyscreen",)
        #t  = F.add(npyscreen.CheckBoxMultiline, max_height=4, name = ["This is a ", "multiline text box."])
        #t  = F.add(npyscreen.CheckBoxMultiline, max_height=4, name = ["This is a second", "multiline text box."])
        t = F.add(MultiSelectWidgetTesting, max_height=7, name="Testing", values=value_list, slow_scroll=False)
        
        # This lets the user play with the Form.
        F.edit()
        
if __name__ == "__main__":
    App = TestApp()
    App.run()   
