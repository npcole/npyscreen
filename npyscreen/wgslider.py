#!/usr/bin/python
import curses
from . import wgwidget     as widget
from . import wgtitlefield as titlefield

class Slider(widget.Widget):
    def __init__(self, screen, value=0, 
                out_of=100, step=1, lowest=0,
                label=True, **keywords):
        self.out_of = out_of
        self.value = value
        self.step = step
        self.lowest = lowest
        super(Slider, self).__init__(screen, **keywords)
        if self.parent.curses_pad.getmaxyx()[0]-1 == self.rely: self.on_last_line = True
        else: self.on_last_line = False
        if self.on_last_line:
            self.maximum_string_length = self.width - 1
        else:   
            self.maximum_string_length = self.width
        self.label = label

    def calculate_area_needed(self):
        return 1,0

    def translate_value(self):
        """What do different values mean?  If you subclass this object, and override this 
        method, you can change how the labels are displayed.  This method should return a
        unicode string, to be displayed to the user. You probably want to ensure this is a fixed width."""
        
        stri = "%s / %s" %(self.value, self.out_of)
        if isinstance(stri, bytes):
            stri = stri.decode(self.encoding, 'replace')
        l = (len(str(self.out_of)))*2+4
        stri = stri.rjust(l)
        return stri
    
    def update(self, clear=True):
        if clear: self.clear()
        if self.hidden:
            self.clear()
            return False
        length_of_display = self.width + 1
        blocks_on_screen = length_of_display

        if self.label:
            label_str = self.translate_value()
            if isinstance(label_str, bytes):
                label_str = label_str.decode(self.encoding, 'replace')
            blocks_on_screen -= len(label_str)+3
            if self.do_colors():
                label_attributes = self.parent.theme_manager.findPair(self)
            else:
                label_attributes = curses.A_NORMAL
            self.add_line(
                self.rely, self.relx+blocks_on_screen+2,
                label_str,
                self.make_attributes_list(label_str, label_attributes),
                len(label_str)
                )
            
            # If want to handle neg. numbers, this line would need changing.
        blocks_to_fill = (float(self.value) / float(self.out_of)) * int(blocks_on_screen)
    
        if self.editing:
            self.parent.curses_pad.attron(curses.A_BOLD)
            #self.parent.curses_pad.bkgdset(curses.ACS_HLINE)
            #self.parent.curses_pad.bkgdset(">")
            #self.parent.curses_pad.bkgdset(curses.A_NORMAL)
            BACKGROUND_CHAR = ">"
            BARCHAR         = curses.ACS_HLINE
        else:
            self.parent.curses_pad.attroff(curses.A_BOLD)
            self.parent.curses_pad.bkgdset(curses.A_NORMAL)
            #self.parent.curses_pad.bkgdset(curses.ACS_HLINE)
            BACKGROUND_CHAR = curses.ACS_HLINE
            BARCHAR         = " "
        
    
        for n in range(blocks_on_screen):
            xoffset = self.relx
            if self.do_colors():
                self.parent.curses_pad.addch(self.rely,n+xoffset, BACKGROUND_CHAR, curses.A_NORMAL | self.parent.theme_manager.findPair(self))
            else:
                self.parent.curses_pad.addch(self.rely,n+xoffset, BACKGROUND_CHAR, curses.A_NORMAL)
    
        for n in range(int(blocks_to_fill)):
            if self.do_colors():
                self.parent.curses_pad.addch(self.rely,n+xoffset, BARCHAR, curses.A_STANDOUT | self.parent.theme_manager.findPair(self))
            else:
                self.parent.curses_pad.addch(self.rely,n+xoffset, BARCHAR, curses.A_STANDOUT) #curses.ACS_BLOCK)

        self.parent.curses_pad.attroff(curses.A_BOLD)
        self.parent.curses_pad.bkgdset(curses.A_NORMAL)
    
    def set_value(self, val):
        #"We can only represent ints or floats, and must be less than what we are out of..."
        if val is None: val = 0
        if not isinstance(val, int) and not isinstance(val, float):
            raise ValueError

        else:
            self.__value = val

        if self.__value > self.out_of: raise ValueError

    def get_value(self):
        return float(self.__value)
    value = property(get_value, set_value)

    def set_up_handlers(self):
        super(widget.Widget, self).set_up_handlers()
        
        self.handlers.update({ 
                    curses.KEY_LEFT: self.h_decrease,
                    curses.KEY_RIGHT: self.h_increase,
                    ord('+'): self.h_increase,
                    ord('-'): self.h_decrease,
                    ord('h'): self.h_decrease,
                    ord('l'): self.h_increase,
                    ord('j'): self.h_exit_down,
                    ord('k'): self.h_exit_up,
                })

    def h_increase(self, ch):
        if (self.value + self.step <= self.out_of): self.value += self.step

    def h_decrease(self, ch):
        if (self.value - self.step >= self.lowest): self.value -= self.step

#   def create_subwindows(self):
#       maximum_possible = self.space_available()[1]
#       
#       if self.request_width:
#           if self.request_width > maximum_possible: ask_for = maximum_possible
#           else: ask_for = self.request_width
#       else:
#           ask_for = maximum_possible
#           
#       self.textfield = self.parent.curses_pad.derwin(1, ask_for, self.rely, self.relx)

class TitleSlider(titlefield.TitleText):
    _entry_type = Slider
    
