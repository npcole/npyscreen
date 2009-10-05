#!/usr/bin/python
import curses
from . import wgwidget    as widget
from . import wgcheckbox  as checkbox

class MiniButton(checkbox._ToggleControl):
    def __init__(self, screen, name='Button', *args, **keywords):
        self.name = self.safe_string(name)
        self.label_width = len(name) + 2
        super(MiniButton, self).__init__(screen, *args, **keywords)
        
    def calculate_area_needed(self):
        return 1, self.label_width+2

    def update(self, clear=True):
        if clear: self.clear()
        if self.hidden:
            self.clear()
            return False
        
        
        if self.value and self.do_colors():
            self.parent.curses_pad.addstr(self.rely, self.relx, '>', self.parent.theme_manager.findPair(self))
            self.parent.curses_pad.addstr(self.rely, self.relx+self.width-1, '<', self.parent.theme_manager.findPair(self))
        elif self.value:
            self.parent.curses_pad.addstr(self.rely, self.relx, '>')
            self.parent.curses_pad.addstr(self.rely, self.relx+self.width-1, '<')
            
        
        if self.editing:
            button_state = curses.A_STANDOUT
        else:
            button_state = curses.A_NORMAL
        
        str = self.name.center(self.label_width)
        if self.do_colors():
            self.parent.curses_pad.addnstr(self.rely, self.relx+1, str, self.label_width, self.parent.theme_manager.findPair(self, 'CONTROL') | button_state)
        else:
            self.parent.curses_pad.addnstr(self.rely, self.relx+1, str, self.label_width, button_state) 
        

class MiniButtonPress(MiniButton):
    def h_tottle(self):
        self.value = True
        self.display()
        self.whenPressed()
        self.value = False
        self.display()
    
    def whenPressed(self):
        pass
