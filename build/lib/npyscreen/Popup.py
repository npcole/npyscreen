#!/usr/bin/python
# encoding: utf-8

import sys
import os
import Form
import ActionForm
import curses

class Popup(Form.Form):
    def __init__(self, lines = 12, columns=60,
        minimum_lines=None,
        minimum_columns=None,
        *args, **keywords):
        super(Popup, self).__init__(lines = lines, columns=columns, 
                                        minimum_columns=40, minimum_lines=8, *args, **keywords)
        self.show_atx = 10
        self.show_aty = 2
        
class ActionPopup(ActionForm.ActionForm, Popup):
    def __init__(self, *args, **keywords):
        Popup.__init__(self, *args, **keywords)
        
class MessagePopup(Popup):
    def __init__(self, *args, **keywords):
        import multiline 
        super(MessagePopup, self).__init__(*args, **keywords)
        self.TextWidget = self.add(multiline.Pager, scroll_exit=True, max_height=self.widget_useable_space()[0]-2)
        
def main(*args):
    import titlefield
    import textbox
    import slider
    import multiline
    

    F = Popup(name="Testing")
    w = F.add_widget(titlefield.TitleText)
    str = "useable space = %s, %s; my height and width is: %s, %s" % (F.widget_useable_space()[0], F.widget_useable_space()[1], w.height, w.width)
    w.value = str
    F.nextrely += 1
    s = F.add_widget(slider.Slider, out_of=10)
    F.edit()

def MessageTest(*args):
    F = MessagePopup()
    F.TextWidget.values = ["This is a ", "very quick test", "of a very useful", "widget", "One","Two","Three","Four","Five"]
    F.edit()

if __name__ == '__main__':
    import curses.wrapper
    from Form import *
    curses.wrapper(MessageTest)

