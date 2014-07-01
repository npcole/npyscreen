#!/usr/bin/env python
# encoding: utf-8
import npyscreen
#npyscreen.disableColor()


class TestApp(npyscreen.NPSApp):
    def main(self):
        F  = npyscreen.Form(name = "Welcome to Npyscreen",)
        
        classification = F.add(npyscreen.MultiLineEditableBoxed,
                        max_height=4,
                        name='Classification:',
                        #footer="Press i or o to insert values", 
                        slow_scroll=True)
        
        #F.nextrely += 1
        
        
        subject = F.add(npyscreen.MultiLineEditableBoxed,
                        max_height=4,
                        name='Subject:',
                        #footer="Press i or o to insert values", 
                        slow_scroll=True)
        
        #F.nextrely += 1
        
        to = F.add(npyscreen.MultiLineEditableBoxed,
                        max_height=6,
                        name='To:',
                        #footer="Press i or o to insert values",
                        scroll_exit=True)
                        
        cc = F.add(npyscreen.MultiLineEditableBoxed,
                        max_height=6,
                        name='CC:',
                        #footer="Press i or o to insert values", 
                        scroll_exit=True)
        
        bcc = F.add(npyscreen.MultiLineEditableBoxed,
                        max_height=6,
                        name='BCC:',
                        #footer="Press i or o to insert values", 
                        slow_scroll=True)
        
        
        
        # This lets the user play with the Form.
        F.edit()
        
if __name__ == "__main__":
    App = TestApp()
    App.run()   
