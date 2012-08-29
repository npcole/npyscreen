#!/usr/bin/python

from .wgtextbox import Textfield
from .wgwidget import Widget
from . import wgwidget as widget
import curses

class _ToggleControl(Widget):
    def set_up_handlers(self):
        super(_ToggleControl, self).set_up_handlers()
        
        self.handlers.update({
                curses.ascii.SP: self.h_toggle,
                ord('x'):        self.h_toggle,
                curses.ascii.NL: self.h_select_exit,
                ord('j'):        self.h_exit_down,
                ord('k'):        self.h_exit_up,
                ord('h'):        self.h_exit_left,
                ord('l'):        self.h_exit_right,                      
            })
    
    def h_toggle(self, ch):
        if self.value is False or self.value is None or self.value == 0: 
            self.value = True
        else: 
            self.value = False
        self.whenToggled()
    
    def whenToggled(self):
        pass
    
    def h_select_exit(self, ch):
        if not self.value:
            self.h_toggle(ch)
        self.editing = False
        self.how_exited = widget.EXITED_DOWN



class Checkbox(_ToggleControl):

    False_box = '[ ]'
    True_box  = '[X]'
    
    def __init__(self, screen, value = False, **keywords):
        self.value = value
        super(Checkbox, self).__init__(screen, **keywords)
        
        self.label_area = Textfield(screen, rely=self.rely, relx=self.relx+5, 
                      width=self.width-5, value=self.name)
        self.show_bold = False
        self.highlight = False
        self.important = False
        self.hide      = False

    def update(self, clear=True):
        if clear: self.clear()
        if self.hidden:
            self.clear()
            return False
        if self.hide: return True

        self.label_area.value = self.name
        
        if self.value:
            cb_display = self.__class__.True_box
        else:
            cb_display = self.__class__.False_box
        
        if self.do_colors():    
            self.parent.curses_pad.addstr(self.rely, self.relx, cb_display, self.parent.theme_manager.findPair(self, 'CONTROL'))
        else:
            self.parent.curses_pad.addstr(self.rely, self.relx, cb_display)


        if self.editing:
            self.label_area.highlight = True
        else:
            self.label_area.highlight = False
        
        if self.show_bold: 
            self.label_area.show_bold = True
        else: 
            self.label_area.show_bold = False
            
        if self.important:
            self.label_area.important = True
        else:
            self.label_area.important = False

        if self.highlight: 
            self.label_area.highlight = True
        else: 
            self.label_area.highlight = False

        self.label_area.update(clear=clear)
        
    def calculate_area_needed(self):
        return 1,0

        
class RoundCheckBox(Checkbox):
    False_box = '( )'
    True_box  = '(X)'

