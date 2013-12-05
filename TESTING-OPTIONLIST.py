#!/usr/bin/env python
# encoding: utf-8

import npyscreen
#npyscreen.disableColor()
class TestApp(npyscreen.NPSApp):
    def main(self):
        Options = npyscreen.OptionList()
        options = Options.options
        options.append(npyscreen.OptionFreeText('FreeText', value='', documentation="This is some documentation."))
        options.append(npyscreen.OptionMultiChoice('Multichoice', choices=['Choice 1', 'Choice 2', 'Choice 3']))
        options.append(npyscreen.OptionFilename('Filename', ))
        options.append(npyscreen.OptionDate('Date', ))
        options.append(npyscreen.OptionMultiFreeText('Multiline Text', value=''))
        
        Options.reload_from_file('/tmp/test')        
        
        # These lines create the form and populate it with widgets.
        # A fairly complex screen in only 8 or so lines of code - a line for each control.
        F  = npyscreen.Form(name = "Welcome to Npyscreen",)

        ms = F.add(npyscreen.OptionListDisplay, name="Option List", 
                values = options, 
                scroll_exit=True,
                max_height=None)
        
        # This lets the user play with the Form.
        F.edit()
        Options.write_to_file('/tmp/test')

if __name__ == "__main__":
    App = TestApp()
    App.run()   
