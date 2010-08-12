#!/usr/bin/python
import curses
import curses.ascii
import curses.wrapper
from . import wgwidget as widget

class TextfieldBase(widget.Widget):
    def __init__(self, screen, value=None, **keywords):
        try:
            self.value
        except:
            self.value = value or ""
        
        super(TextfieldBase, self).__init__(screen, **keywords)

        self.cursor_position = None
        
        self.show_bold = False
        self.highlight = False
        self.important = False
        
        self.syntax_highlighting = False
        self._highlightingdata   = None
        
        self.begin_at = 0   # Where does the display string begin?
        
        if self.on_last_line:
            self.maximum_string_length = self.width - 2  # Leave room for the cursor
        else:   
            self.maximum_string_length = self.width - 1  # Leave room for the cursor at the end of the string.

        self.update()
    
    def calculate_area_needed(self):
        "Need one line of screen, and any width going"
        return 1,0

    def update(self, clear=True, cursor=True):
        """Update the contents of the textbox, without calling the final refresh to the screen"""
        # cursor not working. See later for a fake cursor
        #if self.editing: pmfuncs.show_cursor()
        #else: pmfuncs.hide_cursor()

        # Not needed here -- gets called too much!
        #pmfuncs.hide_cursor()

        if clear: self.clear()

        if self.begin_at < 0: self.begin_at = 0

        if self.editing:
            if cursor:
                if self.cursor_position is False:
                    self.cursor_position = len(self.value)

                elif self.cursor_position > len(self.value):
                    self.cursor_position = len(self.value)

                elif self.cursor_position < 0:
                    self.cursor_position = 0

                if self.cursor_position < self.begin_at:
                    self.begin_at = self.cursor_position

                while self.cursor_position > self.begin_at + self.maximum_string_length: # -1:
                    self.begin_at += 1
            else:
                self.parent.curses_pad.bkgdset(' ',curses.A_STANDOUT)




        if self.highlight:
            self.parent.curses_pad.bkgdset(' ',curses.A_STANDOUT)

        if self.show_bold:
            self.parent.curses_pad.attron(curses.A_BOLD)
        if self.important and not self.do_colors():
            self.parent.curses_pad.attron(curses.A_UNDERLINE)


        self._print()

        # reset everything to normal
        self.parent.curses_pad.attroff(curses.A_BOLD)
        self.parent.curses_pad.attroff(curses.A_UNDERLINE)
        self.parent.curses_pad.bkgdset(' ',curses.A_NORMAL)

        if self.editing and cursor:
            # Cursors do not seem to work on pads.
            #self.parent.curses_pad.move(self.rely, self.cursor_position - self.begin_at)
            # let's have a fake cursor
            _cur_loc_x = self.cursor_position - self.begin_at + self.relx
            # The following two lines work fine for ascii, but not for unicode
            #char_under_cur = self.parent.curses_pad.inch(self.rely, _cur_loc_x)
            #self.parent.curses_pad.addch(self.rely, self.cursor_position - self.begin_at + self.relx, char_under_cur, curses.A_STANDOUT)
            #The following appears to work for unicode as well.
            try:
                char_under_cur = self.safe_string(self.value[self.cursor_position])
            except:
                char_under_cur = ' '

            self.parent.curses_pad.addstr(self.rely, self.cursor_position - self.begin_at + self.relx, char_under_cur, curses.A_STANDOUT)

    def _print(self):
        string_to_print = self.safe_string(self.value)
        if string_to_print == None: return
        
        if self.syntax_highlighting:
            try:
                highlight = self._highlightingdata[self.begin_at+i]
            except:
                highlight = curses.A_NORMAL
            self.update_highlighting(start=self.begin_at, end=self.maximum_string_length+self.begin_at)
            for i in range(len(string_to_print[self.begin_at:self.maximum_string_length+self.begin_at])):
                self.parent.curses_pad.addstr(self.rely,self.relx+i, 
                    string_to_print[self.begin_at+i], 
                    highlight 
                    )
        
        elif self.do_colors():
            coltofind = 'DEFAULT'
            if self.show_bold and self.color == 'DEFAULT':
                coltofind = 'BOLD'
            if self.show_bold:
                self.parent.curses_pad.addstr(self.rely,self.relx, string_to_print[self.begin_at:self.maximum_string_length+self.begin_at], 
                                                    self.parent.theme_manager.findPair(self, coltofind) | curses.A_BOLD)
            elif self.important:
                coltofind = 'IMPORTANT'
                self.parent.curses_pad.addstr(self.rely,self.relx, string_to_print[self.begin_at:self.maximum_string_length+self.begin_at], 
                                                    self.parent.theme_manager.findPair(self, coltofind) | curses.A_BOLD)
            else:
                self.parent.curses_pad.addstr(self.rely,self.relx, string_to_print[self.begin_at:self.maximum_string_length+self.begin_at], 
                                                self.parent.theme_manager.findPair(self))
        else:
            if self.important:
                self.parent.curses_pad.addstr(self.rely,self.relx, 
                        string_to_print[self.begin_at:self.maximum_string_length+self.begin_at], curses.A_BOLD)
            elif self.show_bold:
                self.parent.curses_pad.addstr(self.rely,self.relx, 
                        string_to_print[self.begin_at:self.maximum_string_length+self.begin_at], curses.A_BOLD)

            else:
                self.parent.curses_pad.addstr(self.rely,self.relx, 
                    string_to_print[self.begin_at:self.maximum_string_length+self.begin_at])
    
    def update_highlighting(self, start=None, end=None, clear=False):
        if clear or (self._highlightingdata == None):
            self._highlightingdata = []
        
        string_to_print = self.safe_string(self.value)


class Textfield(TextfieldBase):
    def show_brief_message(self, message):
        curses.beep()
        keep_for_a_moment = self.value
        self.value = message
        self.editing=False
        self.display()
        curses.napms(1200)
        self.editing=True
        self.value = keep_for_a_moment
        

    def edit(self):
        self.editing = 1
        self.cursor_position = len(self.value)
        self.parent.curses_pad.keypad(1)
        
        self.old_value = self.value
        
        self.how_exited = False

        while self.editing:
            self.display()
            self.get_and_use_key_press()

        self.begin_at = 0
        self.display()

        return self.how_exited, self.value

    ###########################################################################################
    # Handlers and methods

    def set_up_handlers(self):
        super(Textfield, self).set_up_handlers()    
    
        # For OS X
        del_key = curses.ascii.alt('~')
        
        self.handlers.update({curses.KEY_LEFT:    self.h_cursor_left,
                           curses.KEY_RIGHT:   self.h_cursor_right,
                   curses.KEY_DC:      self.h_delete_right,
                   curses.ascii.DEL:   self.h_delete_left,
                   curses.ascii.BS:    self.h_delete_left,
                   curses.KEY_BACKSPACE: self.h_delete_left,
                   # mac os x curses reports DEL as escape oddly
                   # no solution yet                   
                   "^K":           self.h_erase_right,
                   "^U":           self.h_erase_left,
            })

        self.complex_handlers.extend((
                                             (self.t_input_isprint, self.h_addch),
                                    # (self.t_is_ck, self.h_erase_right),
                        # (self.t_is_cu, self.h_erase_left),
                        ))

    def t_input_isprint(self, input):
        if curses.ascii.isprint(input) and \
        (chr(input) not in '\n\t\r'): 
            return True
        
        else: return False

    def h_addch(self, input):
        if self.editable:
            #self.value = self.value[:self.cursor_position] + curses.keyname(input) \
            #   + self.value[self.cursor_position:]
            #self.cursor_position += len(curses.keyname(input))
            
            # workaround for the metamode bug:
            self.value = self.value[:self.cursor_position] + chr(input) \
                + self.value[self.cursor_position:]
            self.cursor_position += len(chr(input))

            # or avoid it entirely:
            #self.value = self.value[:self.cursor_position] + curses.ascii.unctrl(input) \
            #   + self.value[self.cursor_position:]
            #self.cursor_position += len(curses.ascii.unctrl(input))

    def h_cursor_left(self, input):
        self.cursor_position -= 1

    def h_cursor_right(self, input):
        self.cursor_position += 1

    def h_delete_left(self, input):
        if self.editable and self.cursor_position > 0:
            self.value = self.value[:self.cursor_position-1] + self.value[self.cursor_position:]
        
        self.cursor_position -= 1
        self.begin_at -= 1

    
    def h_delete_right(self, input):
        if self.editable:
            self.value = self.value[:self.cursor_position] + self.value[self.cursor_position+1:]

    def h_erase_left(self, input):
        if self.editable:
            self.value = self.value[self.cursor_position:]
            self.cursor_position=0
    
    def h_erase_right(self, input):
        if self.editable:
            self.value = self.value[:self.cursor_position]
            self.cursor_postition = len(self.value)
            self.begin_at = 0
    
class FixedText(TextfieldBase):
    def set_up_handlers(self):
        super(FixedText, self).set_up_handlers()
        self.handlers.update({curses.KEY_LEFT:    self.h_cursor_left,
                           curses.KEY_RIGHT:   self.h_cursor_right,
                           })
    
    
    def h_cursor_left(self, input):
        if self.begin_at > 0:
            self.begin_at -= 1

    def h_cursor_right(self, input):
        if len(self.value) - self.begin_at > self.maximum_string_length:
            self.begin_at += 1

    def update(self, clear=True,):
        super(FixedText, self).update(clear=clear, cursor=False)
    
    def edit(self):
        self.editing = 1
        self.highlight = False
        self.cursor_position = 0
        self.parent.curses_pad.keypad(1)
        
        self.old_value = self.value
        
        self.how_exited = False

        while self.editing:
            self.display()
            self.get_and_use_key_press()

        self.begin_at = 0
        self.highlight = False
        self.display()

        return self.how_exited, self.value

