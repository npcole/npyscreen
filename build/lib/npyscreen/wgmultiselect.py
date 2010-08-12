#!/usr/bin/python
from . import wgmultiline    as multiline
from . import wgselectone    as selectone
from . import wgcheckbox     as checkbox
import curses

class MultiSelect(selectone.SelectOne):
    _contained_widgets = checkbox.Checkbox

    def set_up_handlers(self):
        super(MultiSelect, self).set_up_handlers()
        self.handlers.update({
                    ord("x"):    self.h_select_toggle,
                    curses.ascii.SP: self.h_select_toggle,
                    ord("X"):    self.h_select,
                    "^U":        self.h_select_none,
                })
    
    def h_select_none(self, input):
        self.value = []
    
    def h_select_toggle(self, input):
        if self.cursor_line in self.value:
            self.value.remove(self.cursor_line)
        else:
            self.value.append(self.cursor_line)
    
    def h_set_filtered_to_selected(self, ch):
        self.value = self._filtered_values_cache
    
    def h_select_exit(self, ch):
        if not self.cursor_line in self.value:
            self.value.append(self.cursor_line)
        if self.return_exit:
            self.editing = False
            self.how_exited=True
            
    def get_selected_objects(self):
        if self.value == [] or self.value == None:
            return None
        else:
            return [self.values[x] for x in self.value]
        
class MultiSelectFixed(MultiSelect):
    # This does not allow the user to change Values, but does allow the user to move around.
    # Useful for displaying Data.
    def user_set_value(self, input):
        pass
    
    def set_up_handlers(self):
        super(MultiSelectFixed, self).set_up_handlers()
        self.handlers.update({
            ord("x"):   self.user_set_value,
            ord("X"):   self.user_set_value,
            curses.ascii.SP: self.user_set_value,
            "^U":        self.user_set_value,
            curses.ascii.NL:    self.h_exit_down
            
        })

class TitleMultiSelect(multiline.TitleMultiLine):
    _entry_type = MultiSelect
            
        
        
class TitleMultiSelectFixed(multiline.TitleMultiLine):
    _entry_type = MultiSelectFixed
    
    
