#!/usr/bin/env python
import npyscreen

# This example shows how to display the contents of 
# a dictionary to a user.

class KeyValueLine(npyscreen.AnnotateTextboxBase):
    ANNOTATE_WIDTH = 20
    def getAnnotationAndColor(self):
        if self.value:
            return (self.value[0][0:self.ANNOTATE_WIDTH-2], self.annotation_color)
        else:
            return ('', self.annotation_color)
    
    def display_value(self, vl):
        if vl:
            return self.safe_string(str(vl[1]))
        else:
            return ''
    
class KeyValueMultiline(npyscreen.MultiLine):
    _contained_widgets = KeyValueLine
    def when_parent_changes_value(self):
        self.values = self.parent.value.items()
    
    def display_value(self, vl):
        # pass the real object to subwidgets
        return vl
    
class MyForm(npyscreen.Form):
    def create(self):
        self.wgdisplay = self.add(KeyValueMultiline)
    
class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        mainform = self.addForm("MAIN", MyForm)
        
        test_dict= {}
        for i in range(10000):
            test_dict[str(i)] = 'test %s' % i
        
        
        # The following line is the one you want to replace, I suspect.
        #mainform.set_value(globals().copy())
        mainform.set_value(test_dict)
        
if __name__ == "__main__":
    MyTestApp().run()

    
    
    