import curses
import weakref
from .wgwidget import Widget
from .wgmultiline import MultiLine
class BoxBasic(Widget):
    def __init__(self, screen, footer=None, *args, **keywords):
        super(BoxBasic, self).__init__(screen, *args, **keywords)
        self.footer = footer
    
    def update(self, clear=True):
        if clear: self.clear()
        if self.hidden:
            self.clear()
            return False
        HEIGHT = self.height - 1
        WIDTH  = self.width - 1
        # draw box.
        self.parent.curses_pad.hline(self.rely, self.relx, curses.ACS_HLINE, WIDTH)
        self.parent.curses_pad.hline(self.rely + HEIGHT, self.relx, curses.ACS_HLINE, WIDTH)
        self.parent.curses_pad.vline(self.rely, self.relx, curses.ACS_VLINE, self.height)
        self.parent.curses_pad.vline(self.rely, self.relx+WIDTH, curses.ACS_VLINE, HEIGHT)
        
        # draw corners
        self.parent.curses_pad.addch(self.rely, self.relx, curses.ACS_ULCORNER, )
        self.parent.curses_pad.addch(self.rely, self.relx+WIDTH, curses.ACS_URCORNER, )
        self.parent.curses_pad.addch(self.rely+HEIGHT, self.relx, curses.ACS_LLCORNER, )
        self.parent.curses_pad.addch(self.rely+HEIGHT, self.relx+WIDTH, curses.ACS_LRCORNER, )
        
        # draw title
        if self.name:
            if isinstance(self.name, bytes):
                name = self.name.decode(self.encoding, 'replace')
            else:
                name = self.name
            name = self.safe_string(name)
            name = " " + name + " "
            if isinstance(name, bytes):
                name = name.decode(self.encoding, 'replace')
            name_attributes = curses.A_NORMAL
            if self.do_colors() and not self.editing:
                name_attributes = name_attributes | self.parent.theme_manager.findPair(self, 'LABEL') #| curses.A_BOLD
            elif self.editing:
                name_attributes = name_attributes | self.parent.theme_manager.findPair(self, 'HILIGHT')
            else:
                name_attributes = name_attributes #| curses.A_BOLD
            
            if self.editing:
                name_attributes = name_attributes | curses.A_BOLD
                
            self.add_line(self.rely, self.relx+4, name, 
                self.make_attributes_list(name, name_attributes), 
                self.width-8)
            # end draw title
            
            # draw footer
            if hasattr(self, 'footer') and self.footer:
                footer_text = self.footer
                if isinstance(footer_text, bytes):
                    footer_text = footer_text.decode(self.encoding, 'replace')
                footer_text = self.safe_string(footer_text)
                footer_text = " " + footer_text + " "
                if isinstance(footer_text, bytes):
                    footer_text = footer_text.decode(self.encoding, 'replace')
                
                footer_attributes = self.get_footer_attributes(footer_text)
                if len(footer_text) <= self.width - 4:
                    placing = self.width - 4 - len(footer_text)
                else:
                    placing = 4
            
                self.add_line(self.rely+HEIGHT, self.relx+placing, footer_text, 
                    footer_attributes, 
                    self.width-placing-2)
        
            
    
    def get_footer_attributes(self, footer_text):
        footer_attributes = self.parent.theme_manager.findPair(self, 'LABEL')
        return self.make_attributes_list(footer_text, footer_attributes)
        
        
class BoxTitle(BoxBasic):
    _contained_widget = MultiLine
    def __init__(self, screen, *args, **keywords):
        super(BoxTitle, self).__init__(screen, *args, **keywords)
        self.make_contained_widget()
    
    def make_contained_widget(self):
        self._my_widgets = []
        self._my_widgets.append(self._contained_widget(self.parent, 
         rely=self.rely+1, relx = self.relx+2, 
         max_width=self.width-4, max_height=self.height-2,
         ))
        self.entry_widget = weakref.proxy(self._my_widgets[0])
            
    def update(self, clear=True):
        if self.hidden and clear:
            self.clear()
            return False
        elif self.hidden:
            return False
        super(BoxTitle, self).update(clear=clear)
        for w in self._my_widgets:
            w.update(clear=clear)
    
    def edit(self):
        self.editing=True
        self.display()
        self.entry_widget.edit()
        #self.value = self.textarea.value
        self.how_exited = self.entry_widget.how_exited
        self.editing=False
        self.display()

    
        
    def get_value(self):
        try:
            return self.entry_widget.value
        except:
            try:
                return self.__tmp_value
            except:
                return None
    def set_value(self, value):
        try:
            self.entry_widget.value = value
        except:
            # probably trying to set the value before the textarea is initialised
            self.__tmp_value = value
    def del_value(self):
        del self.entry_widget.value
    value = property(get_value, set_value, del_value)
    
    def get_values(self):
        try:
            return self.entry_widget.values
        except:
            try:
                return self.__tmp_values
            except:
                return None
    def set_values(self, value):
        try:
            self.entry_widget.values = value
        except:
            # probably trying to set the value before the textarea is initialised
            self.__tmp_values = value
    def del_values(self):
        del self.entry_widget.value
    values = property(get_values, set_values, del_values)
    
       
           
       
    