from . import wgtextbox

import unicodedata
import curses



class TextfieldUnicode(wgtextbox.Textfield):
    width_mapping = {'F':2, 'H': 1, 'W': 2, 'Na': 1, 'N': 1}
    def find_apparent_cursor_position(self, ):
        string_to_print = self.display_value(self.value)[self.begin_at:self.maximum_string_length+self.begin_at-self.left_margin]
        cursor_place_in_visible_string = self.cursor_position - self.begin_at
        counter = 0
        columns = 0
        while counter < cursor_place_in_visible_string:
             columns += self.find_width_of_char(string_to_print[counter])
             counter += 1
        return columns
    
    def find_width_of_char(self, char):
        return 1
        w = unicodedata.east_asian_width(char)
        if w == 'A':
            # Abiguous - allow 1, but be aware that this could well be wrong
            return 1
        else:
            return self.__class__.width_mapping[w]
    
    def _print(self):
        string_to_print = self.display_value(self.value)[self.begin_at:self.maximum_string_length+self.begin_at-self.left_margin]
        column = 0
        place_in_string = 0
        if self.syntax_highlighting:
            self.update_highlighting(start=self.begin_at, end=self.maximum_string_length+self.begin_at-self.left_margin)
            while column <= (self.maximum_string_length - self.left_margin):
                if not string_to_print or place_in_string > len(string_to_print)-1:
                    break
                width_of_char_to_print = self.find_width_of_char(string_to_print[place_in_string])
                if column - 1 + width_of_char_to_print > self.maximum_string_length:
                    break 
                try:
                    highlight = self._highlightingdata[self.begin_at+place_in_string]
                except:
                    highlight = curses.A_NORMAL                
                self.parent.curses_pad.addstr(self.rely,self.relx+column+self.left_margin, 
                    string_to_print[place_in_string], 
                    highlight
                    )
                column += self.find_width_of_char(string_to_print[place_in_string])
                place_in_string += 1
        else:
            if self.do_colors():
                if self.show_bold and self.color == 'DEFAULT':
                    color = self.parent.theme_manager.findPair(self, 'BOLD') | curses.A_BOLD
                elif self.show_bold:
                    color = self.parent.theme_manager.findPair(self, self.color) | curses.A_BOLD
                elif self.important:
                    color = self.parent.theme_manager.findPair(self, 'IMPORTANT') | curses.A_BOLD
                else:
                    color = self.parent.theme_manager.findPair(self)
            else:
                if self.important or self.show_bold:
                    color = curses.A_BOLD
                else:
                    color = curses.A_NORMAL
            
            while column <= (self.maximum_string_length - self.left_margin):
                if not string_to_print or place_in_string > len(string_to_print)-1:
                    break
                width_of_char_to_print = self.find_width_of_char(string_to_print[place_in_string])
                if column - 1 + width_of_char_to_print > self.maximum_string_length:
                    break 
                self.parent.curses_pad.addstr(self.rely,self.relx+column+self.left_margin, 
                    string_to_print[place_in_string], 
                    color
                    )
                column += width_of_char_to_print
                place_in_string += 1
            
    def print_cursor(self):
        # This needs fixing for Unicode multi-width chars.

        # Cursors do not seem to work on pads.
        #self.parent.curses_pad.move(self.rely, self.cursor_position - self.begin_at)
        # let's have a fake cursor
        _cur_loc_x = self.cursor_position - self.begin_at + self.relx + self.left_margin
        # The following two lines work fine for ascii, but not for unicode
        #char_under_cur = self.parent.curses_pad.inch(self.rely, _cur_loc_x)
        #self.parent.curses_pad.addch(self.rely, self.cursor_position - self.begin_at + self.relx, char_under_cur, curses.A_STANDOUT)
        #The following appears to work for unicode as well.
        try:
            char_under_cur = self.value[self.cursor_position] #use the real value
            char_under_cur = self.safe_string(char_under_cur)
        except:
            char_under_cur = ' '

        self.parent.curses_pad.addstr(self.rely, self.cursor_position - self.begin_at + self.relx + self.left_margin, char_under_cur, curses.A_STANDOUT)

    def t_input_isprint(self, input):
        if self._last_get_ch_was_unicode:
            if (chr(input) not in '\n\t\r'): 
                return True
            else: 
                return False
        else:
            if curses.ascii.isprint(input) and \
            (chr(input) not in '\n\t\r'): 
                return True
            else: 
                return False
        #if curses.ascii.isprint(input) and \
        if (chr(input) not in '\n\t\r'): 
            return True

        else: return False
        
    def h_addch(self, input):
        if self.editable:
            #self.value = self.value[:self.cursor_position] + curses.keyname(input) \
            #   + self.value[self.cursor_position:]
            #self.cursor_position += len(curses.keyname(input))

            # workaround for the metamode bug:

            ch_adding = chr(input)

            self.value = self.value[:self.cursor_position] + ch_adding \
                + self.value[self.cursor_position:]
            self.cursor_position += len(ch_adding)

    
        
    
