#!/usr/bin/python
import curses
import locale
from . import npysGlobalOptions as GlobalOptions
from . import wgwidget    as widget
from . import wgcheckbox  as checkbox

class MiniButton(checkbox._ToggleControl):
    def __init__(self, screen, name='Button', *args, **keywords):
        self.encoding = 'utf-8'
        if GlobalOptions.ASCII_ONLY or locale.getpreferredencoding() == 'US-ASCII':
            self._force_ascii = True
        else:
            self._force_ascii = False
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
        
        button_name = self.name
        if isinstance(button_name, bytes):
            button_name = button_name.decode(self.encoding, 'replace')
        button_name = button_name.center(self.label_width)
        
        if self.do_colors():
            button_attributes = self.parent.theme_manager.findPair(self, 'CONTROL') | button_state
        else:
            button_attributes = button_state
        
        self.add_line(self.rely, self.relx+1,
            button_name,
            self.make_attributes_list(button_name, button_attributes),
            self.label_width
            )


class MiniButtonPress(MiniButton):
    def h_toggle(self, ch):
        self.value = True
        self.display()
        self.whenPressed()
        self.value = False
        self.display()
    
    def whenPressed(self):
        pass
