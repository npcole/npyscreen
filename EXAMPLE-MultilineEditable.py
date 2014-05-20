#!/usr/bin/env python
# encoding: utf-8
import npyscreen
#npyscreen.disableColor()


class TestApp(npyscreen.NPSApp):
    def main(self):
        value_list = [
           "This is the first",
           "This is the second",
           "This is the third",
           "This is the fourth",
        ]
        F  = npyscreen.Form(name = "Welcome to Npyscreen",)
        t = F.add(npyscreen.MultiLineEditableBoxed,
                        max_height=20,
                        name='List of Values',
                        footer="Press i or o to insert values", 
                        values=value_list, 
                        slow_scroll=False)
        
        # This lets the user play with the Form.
        F.edit()
        
if __name__ == "__main__":
    App = TestApp()
    App.run()   
