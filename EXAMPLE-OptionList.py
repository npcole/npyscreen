#!/usr/bin/env python
# encoding: utf-8


# The system here is an experimental one. See documentation for details.




import npyscreen
class TestApp(npyscreen.NPSApp):
    def main(self):
        Options = npyscreen.OptionList()
        
        # just for convenience so we don't have to keep writing Options.options
        options = Options.options
        
        options.append(npyscreen.OptionFreeText('FreeText', value='', documentation="This is some documentation."))
        options.append(npyscreen.OptionMultiChoice('Multichoice', choices=['Choice 1', 'Choice 2', 'Choice 3']))
        options.append(npyscreen.OptionFilename('Filename', ))
        options.append(npyscreen.OptionDate('Date', ))
        options.append(npyscreen.OptionMultiFreeText('Multiline Text', value=''))
        options.append(npyscreen.OptionMultiFreeList('Multiline List'))
        
        try:
            Options.reload_from_file('/tmp/test')
        except FileNotFoundError:
            pass        
        
        F  = npyscreen.Form(name = "Welcome to Npyscreen",)

        ms = F.add(npyscreen.OptionListDisplay, name="Option List", 
                values = options, 
                scroll_exit=True,
                max_height=None)
        
        F.edit()
        
        Options.write_to_file('/tmp/test')

if __name__ == "__main__":
    App = TestApp()
    App.run()   
