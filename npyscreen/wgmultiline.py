#!/usr/bin/python
import copy
from . import wgwidget       as widget
from . import wgtextbox      as textbox
import curses
from . import wgtitlefield   as titlefield
from . import fmPopup        as Popup
import weakref

MORE_LABEL = "- more -" # string to tell user there are more options

class FilterPopupHelper(Popup.Popup):
    def create(self):
        super(FilterPopupHelper, self).create()
        self.filterbox = self.add(titlefield.TitleText, name='Find:', )
        self.nextrely += 1
        self.statusline = self.add(textbox.Textfield, color = 'LABEL', editable = False)
    
    def updatestatusline(self):
        self.owner_widget._filter   = self.filterbox.value
        filtered_lines = self.owner_widget.get_filtered_indexes()
        len_f = len(filtered_lines)
        if self.filterbox.value == None or self.filterbox.value == '':
            self.statusline.value = ''
        elif len_f == 0: 
            self.statusline.value = '(No Matches)'
        elif len_f == 1:
            self.statusline.value = '(1 Match)'
        else:
            self.statusline.value = '(%s Matches)' % len_f
    
    def adjust_widgets(self):
        self.updatestatusline()
        self.statusline.display()

class MultiLine(widget.Widget):
    """Display a list of items to the user.  By overloading the display_value method, this widget can be made to 
display different kinds of objects.  Given the standard definition, 
the same effect can be achieved by altering the __str__() method of displayed objects"""
    _MINIMUM_HEIGHT = 2 # Raise an error if not given this.
    _contained_widgets = textbox.Textfield
    def __init__(self, screen, values = None, value = None,
            slow_scroll=False, scroll_exit=False, 
            return_exit=False,
            exit_left  = False,
            exit_right = False,
             **keywords):
        
        self.exit_left       = exit_left
        self.exit_right      = exit_right
        super(MultiLine, self).__init__(screen, **keywords)
        if self.height < self.__class__._MINIMUM_HEIGHT:
            raise Exception("Not enough space allowed for %s" % str(self))
        self.make_contained_widgets()

        self.value = value
        
        # does pushing return select and then leave the widget?
        self.return_exit = return_exit
        
        
        self.slow_scroll     = slow_scroll
        self.scroll_exit     = scroll_exit
        
        self.start_display_at = 0
        self.cursor_line = 0
        self.values = values or []
        self._filter = None
        
        #These are just to do some optimisation tricks
        self._last_start_display_at = None
        self._last_cursor_line = None
        self._last_values = copy.copy(values)
        self._last_value = copy.copy(value)
        self._last_filter = None
        self._filtered_values_cache = []

        #override - it looks nicer.
        if self.scroll_exit: self.slow_scroll=True
    
    
    def make_contained_widgets(self, ):
        self._my_widgets = []
        for h in range(self.height):
            self._my_widgets.append(self._contained_widgets(self.parent, 
             rely=h+self.rely, relx = self.relx, 
             max_width=self.width, max_height=1))


    def display_value(self, vl):
        """Overload this function to change how values are displayed.  
Should accept one argument (the object to be represented), and return a string."""
        return str(vl)

    def calculate_area_needed(self):
        return 0,0
        
    
    def reset_cursor(self):
        self.start_display_at = 0
        self.cursor_line      = 0
    
    
    def update(self, clear=True):
        if self.hidden:
            self.clear()
            return False
            
        if self.values == None:
            self.values = []
            
        # clear = None is a good value for this widget
        display_length = len(self._my_widgets)
        self._remake_filter_cache()
        self._filtered_values_cache = self.get_filtered_indexes()

        if self.editing:
            if self.cursor_line < 0: self.cursor_line = 0
            if self.cursor_line > len(self.values)-1: self.cursor_line = len(self.values)-1
            
            if self.slow_scroll:
                if self.cursor_line > self.start_display_at+display_length-1:
                    self.start_display_at = self.cursor_line - (display_length-1) 

                if self.cursor_line < self.start_display_at:
                    self.start_display_at = self.cursor_line
            
            else:
                if self.cursor_line > self.start_display_at+(display_length-1):
                    self.start_display_at = self.cursor_line

                if self.cursor_line < self.start_display_at:
                    self.start_display_at = self.cursor_line - (display_length-2)
                    if self.start_display_at < 0: self.start_display_at=0
        
        # What this next bit does is to not bother updating the screen if nothing has changed.
        no_change = False
        try:            
            if ( self._last_value is self.value) and \
                (self.values == self._last_values) and \
                (self.start_display_at == self._last_start_display_at) and \
                (clear != True) and \
                (self._last_cursor_line == self.cursor_line) and \
                (self._last_filter == self._filter) and \
                self.editing:
                no_change = True
       
            else:
                no_change = False
        except:
                no_change = False
            
        if not no_change:
            if clear is True: 
                self.clear()

            if (self._last_start_display_at != self.start_display_at) \
                    and clear is None:
                self.clear()
            else:
                pass

            self._last_start_display_at = self.start_display_at
            

            indexer = 0 + self.start_display_at
            for line in self._my_widgets[:-1]:
                self._print_line(line, indexer)
                line.task = "PRINTLINE"
                line.update(clear=False)
                indexer += 1
        
            # Now do the final line
            line = self._my_widgets[-1]
            
            if len(self.values) <= indexer+1:
                self._print_line(line, indexer)
                line.task="PRINTLINE"
                line.update(clear=False)
            else:
                line.value = MORE_LABEL
                line.name = MORE_LABEL
                line.task = MORE_LABEL
                #line.highlight = False
                #line.show_bold = False
                line.clear()
                if self.do_colors():
                    self.parent.curses_pad.addstr(self.rely+self.height-1, self.relx, MORE_LABEL, self.parent.theme_manager.findPair(self, 'CONTROL'))
                else:
                    self.parent.curses_pad.addstr(self.rely+self.height-1, self.relx, MORE_LABEL)
        
            if self.editing: 
                self._my_widgets[(self.cursor_line-self.start_display_at)].highlight=True
                self._my_widgets[(self.cursor_line-self.start_display_at)].update(clear=True)


        self._last_start_display_at = self.start_display_at
        self._last_cursor_line = self.cursor_line
        self._last_values = copy.copy(self.values)
        self._last_value  = copy.copy(self.value)
        


    def _print_line(self, line, value_indexer):
            try:
                line.value = self.display_value(self.values[value_indexer])
                line.hide = False
            except IndexError:
                line.value = None
                line.show_bold=False
                line.name = None
                line.hide = True
            except TypeError:
                line.value = None
                line.show_bold=False
                line.name = None
                line.hide = True
                
                
            
            if value_indexer in self._filtered_values_cache:
                line.important = True
            else:
                line.important = False
            
            if (value_indexer == self.value) and \
                (self.value is not None):
                line.show_bold=True
            else: line.show_bold=False
        
            line.highlight=False
            

    def get_filtered_indexes(self):
        if self._filter == None or self._filter == '':
            return []
        list_of_indexes = []
        for indexer in range(len(self.values)):
            if self.filter_value(indexer):
                list_of_indexes.append(indexer)
        return list_of_indexes
    
    def get_filtered_values(self):
        fvls = []
        for vli in self.get_filtered_indexes():
            fvls.append(self.values[vli])
        return fvls
    
    def _remake_filter_cache(self):
        self._filtered_values_cache = self.get_filtered_indexes()
        

    def filter_value(self, index):
        if self._filter in self.display_value(self.values[index]):
            return True
        else:
            return False
            
    def jump_to_first_filtered(self, ):
        self.h_cursor_beginning(None)
        self.move_next_filtered(include_this_line=True)

    def clear_filter(self):
        self._filter = None
        self.cursor_line = 0
        self.start_display_at = 0

    def move_next_filtered(self, include_this_line=False, *args):
        if self._filter == None:
            return False
        for possible in self._filtered_values_cache:
            if (possible==self.cursor_line and include_this_line==True):
                self.update()
                break
            elif possible > self.cursor_line:
                self.cursor_line = possible
                self.update()
                break
        if self.cursor_line-self.start_display_at > len(self._my_widgets) or \
        self._my_widgets[self.cursor_line-self.start_display_at].task == MORE_LABEL: 
            if self.slow_scroll:
                self.start_display_at += 1
            else:
                self.start_display_at = self.cursor_line
        
    def move_previous_filtered(self, *args):
        if self._filter == None:
            return False
        nextline = self.cursor_line
        _filtered_values_cache_reversed = copy.copy(self._filtered_values_cache)
        _filtered_values_cache_reversed.reverse()
        for possible in _filtered_values_cache_reversed:
            if possible < self.cursor_line:
                self.cursor_line = possible
                return True
                break


    def set_up_handlers(self):
        super(MultiLine, self).set_up_handlers()
        self.handlers.update ( {
                    curses.KEY_UP:      self.h_cursor_line_up,
                    ord('k'):       self.h_cursor_line_up,
                    curses.KEY_LEFT:    self.h_cursor_line_up,
                    curses.KEY_DOWN:    self.h_cursor_line_down,
                    ord('j'):       self.h_cursor_line_down,
                    curses.KEY_RIGHT:   self.h_cursor_line_down,
                    curses.KEY_NPAGE:   self.h_cursor_page_down,
                    curses.KEY_PPAGE:   self.h_cursor_page_up,
                    curses.ascii.TAB:   self.h_exit_down,
                    curses.ascii.NL:    self.h_select_exit,
                    curses.KEY_HOME:    self.h_cursor_beginning,
                    curses.KEY_END:     self.h_cursor_end,
                    ord('g'):       self.h_cursor_beginning,
                    ord('G'):       self.h_cursor_end,
                    ord('x'):       self.h_select,
                    ord('l'):       self.h_set_filter,
                    ord('L'):       self.h_clear_filter,
                    ord('n'):       self.move_next_filtered,
                    ord('N'):       self.move_previous_filtered,
                    ord('p'):       self.move_previous_filtered,
                    "^L":        self.h_set_filtered_to_selected,
                    curses.ascii.SP:    self.h_select,
                    curses.ascii.ESC:   self.h_exit,
                } )
                
        if self.exit_left:
            self.handlers.update({
                    curses.KEY_LEFT:    self.h_exit_left
            })
        
        if self.exit_right:
            self.handlers.update({
                    curses.KEY_RIGHT:   self.h_exit_right
            })

        self.complex_handlers = [
                    #(self.t_input_isprint, self.h_find_char)
                    ]
    
    def h_find_char(self, input):
        # The following ought to work, but there is a curses keyname bug
        # searchingfor = curses.keyname(input).upper()
        # do this instead:
        searchingfor = chr(input).upper()
        for counter in range(len(self.values)):
            try:
                if self.values[counter].find(searchingfor) is not -1:
                    self.cursor_line = counter
                    break
            except AttributeError:
                break

    def t_input_isprint(self, input):
        if curses.ascii.isprint(input): return True
        else: return False
    
    def h_set_filter(self, ch):
        P = FilterPopupHelper()
        P.owner_widget = weakref.proxy(self)
        P.display()
        P.filterbox.edit()
        self._remake_filter_cache()
        self.jump_to_first_filtered()
        
    def h_clear_filter(self, ch):
        self.clear_filter()
        self.display()
    
    def h_cursor_beginning(self, ch):
        self.cursor_line = 0
    
    def h_cursor_end(self, ch):
        self.cursor_line= len(self.values)

    def h_cursor_page_down(self, ch):
        self.cursor_line += (len(self._my_widgets)-1) # -1 because of the -more-
        if self.cursor_line >= len(self.values)-1:
            self.cursor_line = len(self.values) -1
        if not (self.start_display_at + len(self._my_widgets) -1 ) > len(self.values):
            self.start_display_at += (len(self._my_widgets)-1)
            if self.start_display_at > len(self.values) - (len(self._my_widgets)-1):
                self.start_display_at = len(self.values) - (len(self._my_widgets)-1)
    
    def h_cursor_page_up(self, ch):
        self.cursor_line -= (len(self._my_widgets)-1)
        if self.cursor_line < 0:
            self.cursor_line = 0
        self.start_display_at -= (len(self._my_widgets)-1)
        if self.start_display_at < 0: self.start_display_at = 0
                    
    def h_cursor_line_up(self, ch):
        self.cursor_line -= 1
        if self.cursor_line < 0: 
            if self.scroll_exit:
                self.cursor_line = 0
                self.h_exit_up(ch)
            else: 
                self.cursor_line = 0

    def h_cursor_line_down(self, ch):
        self.cursor_line += 1
        if self.cursor_line >= len(self.values):
            if self.scroll_exit: 
                self.cursor_line = len(self.values)-1
                self.h_exit_down(ch)
                return True
            else: 
                self.cursor_line -=1
                return True

        if self._my_widgets[self.cursor_line-self.start_display_at].task == MORE_LABEL: 
            if self.slow_scroll:
                self.start_display_at += 1
            else:
                self.start_display_at = self.cursor_line
        
    def h_exit(self, ch):
        self.editing = False
        self.how_exited = True
    
    def h_set_filtered_to_selected(self, ch):
        if len(self._filtered_values_cache) < 2:
            self.value = self._filtered_values_cache
        else:
            # There is an error - trying to select too many things.
            curses.beep()
    
    def h_select(self, ch):
        self.value = self.cursor_line

    def h_select_exit(self, ch):
        self.h_select(ch)
        if self.return_exit:
            self.editing = False
            self.how_exited=True


    def edit(self):
        self.editing = True
        self.how_exited = None
        #if self.value: self.cursor_line = self.value
        self.display()
        while self.editing:
            self.get_and_use_key_press()
            self.update(clear=None)
##          self.clear()
##          self.update(clear=False)
            self.parent.refresh()
##          curses.napms(10)
##          curses.flushinp()

class Pager(MultiLine):
    def update(self, clear=True):
        #we look this up a lot. Let's have it here.
        display_length = len(self._my_widgets)
    
        if self.start_display_at > len(self.values) - display_length: 
            self.start_display_at = len(self.values) - display_length
        if self.start_display_at < 0: self.start_display_at = 0
        
        indexer = 0 + self.start_display_at
        for line in self._my_widgets[:-1]: 
            self._print_line(line, indexer)
            indexer += 1
        
        # Now do the final line
        line = self._my_widgets[-1]
            
        if len(self.values) <= indexer+1:
            self._print_line(line, indexer)
        else:
            line.value = MORE_LABEL
            line.highlight = False
            line.show_bold = False
        
        for w in self._my_widgets: 
            # call update to avoid needless refreshes
            w.update(clear=True)
            
            
    def get_selected_objects(self):
        if self.value == None:
            return None
        else:
            return self.values[self.value]
            
    def edit(self):
        # Make sure a value never gets set.
        value = self.value
        super(Pager, self).edit()
        self.value = value
    
    def h_scroll_line_up(self, input):
        self.start_display_at -= 1

    def h_scroll_line_down(self, input):
        self.start_display_at += 1  

    def h_scroll_page_down(self, input):
        self.start_display_at += len(self._my_widgets)

    def h_scroll_page_up(self, input):
        self.start_display_at -= len(self._my_widgets)

    def h_show_beginning(self, input):
        self.start_display_at = 0   
    
    def h_show_end(self, input):
        self.start_display_at = len(self.values) - len(self._my_widgets)
    
    def h_select_exit(self, input):
        self.exit(self, input)
    
    def set_up_handlers(self):
        super(Pager, self).set_up_handlers()
        self.handlers = {
                    curses.KEY_UP:      self.h_scroll_line_up,
                    curses.KEY_LEFT:    self.h_scroll_line_up,
                    curses.KEY_DOWN:    self.h_scroll_line_down,
                    curses.KEY_RIGHT:   self.h_scroll_line_down,
                    curses.KEY_NPAGE:   self.h_scroll_page_down,
                    curses.KEY_PPAGE:   self.h_scroll_page_up,
                    curses.KEY_HOME:    self.h_show_beginning,
                    curses.KEY_END:     self.h_show_end,
                    curses.ascii.NL:    self.h_exit,
                    curses.ascii.SP:    self.h_scroll_page_down,
                    curses.ascii.TAB:   self.h_exit,
                    ord('x'):       self.h_exit,
                    ord('q'):       self.h_exit,
                    curses.ascii.ESC:   self.h_exit,
                }

        self.complex_handlers = [
                    ]

class TitleMultiLine(titlefield.TitleText):
    _entry_type = MultiLine

    def get_selected_objects(self):
        return self.entry_widget.get_selected_objects()

    def get_values(self):
        try:
            return self.entry_widget.values
        except:
            try:
                return self.__tmp_values
            except:
                return None
    
    def set_values(self, values):
        try:
            self.entry_widget.values = values
        except:
            # probably trying to set the value before the textarea is initialised
            self.__tmp_values = values

    def del_values(self):
        del self.entry_widget.values
    
    values = property(get_values, set_values, del_values)


