from . import fmForm

# TOTALLY BROKEN AND UNFINISHED
# DON'T USE





class ActionFormNew(fmForm.FormBaseNew):
    CANCEL_BUTTON_BR_OFFSET = (2, 12)
    OK_BUTTON_TEXT          = "OK"
    CANCEL_BUTTON_TEXT      = "Cancel"
    
    def __init__(self, *args, **keywords):
        super(ActionFormNew, self).__init__(*args, **keywords)
        self._added_buttons = {}
    
    def set_up_exit_condition_handlers(self):
        super(ActionForm, self).set_up_exit_condition_handlers()
        self.how_exited_handers.update({
            widget.EXITED_ESCAPE:   self.find_cancel_button
        })

    def find_cancel_button(self):
        self.editw = len(self._widgets__)-2
    
    def on_cancel(self):
        pass
    
    def on_ok(self):
        pass
    
    
    
    def _add_button(self, button_name, button_type, button_text, button_rely, button_relx, button_function):
        tmp_rely, tmp_relx = self.nextrely, self.nextrelx
        
        self._added_buttons[button_name] = self.add_widget(button_type, name=button_text, rely=button_rely, relx=button_relx, use_max_space=True)
        
        
        self.nextrely, self.nextrelx = tmp_rely, tmp_relx
    
    
    
    
    
    
    def move_ok_button(self):
        super(ActionFormNew, self).move_ok_button()
        if hasattr(self, 'c_button'):
            c_button_text = self.CANCEL_BUTTON_TEXT
            cmy, cmx = self.curses_pad.getmaxyx()
            cmy -= self.__class__.CANCEL_BUTTON_BR_OFFSET[0]
            cmx -= len(c_button_text)+self.__class__.CANCEL_BUTTON_BR_OFFSET[1]
            self.c_button.rely = cmy
            self.c_button.relx = cmx
    
    def _add_ok_button(self):
        tmp_rely, tmp_relx = self.nextrely, self.nextrelx
        my, mx = self.curses_pad.getmaxyx()
        ok_button_text = self.__class__.OK_BUTTON_TEXT
        my -= self.__class__.OK_BUTTON_BR_OFFSET[0]
        mx -= len(ok_button_text)+self.__class__.OK_BUTTON_BR_OFFSET[1]
        self.ok_button = self.add_widget(self.__class__.OKBUTTON_TYPE, name=ok_button_text, rely=my, relx=mx, use_max_space=True)
        self.ok_button_postion = len(self._widgets__)-1
        self.ok_button.update()
    
    def _destroy_ok_button(self):
        self.ok_button.destroy()
        del self._widgets__[self.ok_button_postion]
        del self.ok_button
        self.display()
    
    def pre_edit_loop(self):
        self.tmp_rely, self.tmp_relx = self.nextrely, self.nextrelx
        
    def post_edit_loop(self):
        self.nextrely, self.nextrelx = tmp_rely, tmp_relx
        
    def _during_edit_loop(self):
        pass
