#!/usr/bin/python
import curses
import weakref
from . import wgtextbox  as textbox
from . import wgwidget   as widget

class TitleText(widget.Widget):
    
    _entry_type = textbox.Textfield


    def __init__(self, screen, 
        begin_entry_at = 16, 
        field_width = None,
        value = None,
        use_two_lines = None,
        hidden=False,
        labelColor='LABEL',
        allow_override_begin_entry_at=True,
        **keywords):
        
        self.hidden = hidden
        self.text_field_begin_at = begin_entry_at
        self.field_width_request = field_width
        self.labelColor = labelColor
        super(TitleText, self).__init__(screen, **keywords)
    
        if self.name is None: self.name = 'NoName'

        if use_two_lines is None:
            if len(self.name)+2 >= begin_entry_at: self.use_two_lines = True
            else: self.use_two_lines = False
        else: self.use_two_lines = use_two_lines

        self.label_widget = textbox.Textfield(screen, relx=self.relx, rely=self.rely, width=len(self.name)+1, value=self.name, color=self.labelColor)
        if self.label_widget.on_last_line and self.use_two_lines:
            # we're in trouble here.
            if len(self.name) > 12: ab_label = 12
            else: ab_label = len(self.name)
            self.use_two_lines = False
            self.label_widget = textbox.Textfield(screen, relx=self.relx, rely=self.rely, width=ab_label+1, value=self.name)
            if allow_override_begin_entry_at:
                self.text_field_begin_at = ab_label + 1
        if self.use_two_lines: tmp_y = 1
        else: tmp_y = 0
        passon = keywords.copy()
        for dangerous in ('relx', 'rely','value',):# 'width','max_width'):
            try:
                passon.pop(dangerous)
            except:
                pass
        try:
            if self.field_width_request:
                passon['width'] = self.field_width_request
            else:
                try:
                    if passon['max_width']:
                        passon['max_width'] -= self.text_field_begin_at+1
                except:
                    pass
                try:
                    if passon['width']:
                        passon['width'] -= self.text_field_begin_at+1
                except:
                    pass
        except:
            pass
                
        self.entry_widget = self.__class__._entry_type(screen, relx=(self.relx + self.text_field_begin_at), 
                                rely=(self.rely+tmp_y), value = value,
                                **passon)
        self.entry_widget.parent_widget = weakref.proxy(self)
        self.recalculate_size()
    
    def recalculate_size(self):
        self.height = self.entry_widget.height
        if self.use_two_lines: self.height += 1
        else: pass
        self.width = self.entry_widget.width + self.text_field_begin_at
    
    def edit(self):
        self.editing=True
        self.display()
        self.entry_widget.edit()
        #self.value = self.textarea.value
        self.how_exited = self.entry_widget.how_exited
        self.editing=False
        self.display()

    def update(self, clear = True):
        if clear: self.clear()
        if self.hidden: return False
        if self.editing: 
            self.label_widget.show_bold = True
            self.label_widget.color = 'LABELBOLD'
        else: 
            self.label_widget.show_bold = False
            self.label_widget.color = self.labelColor
        self.label_widget.update()
        self.entry_widget.update()  
    
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


class TitleFixedText(TitleText):
    _entry_type = textbox.FixedText
