## Very, very experimental. Do NOT USE.

from . import fmForm

class FormMultiPage(fmForm.FormBaseNew):
    def __init__(self, *args, **keywords):
        super(FormMultiPage, self).__init__(*args, **keywords)
        self.switch_page(0)
    
    def _clear_all_widgets(self,):
        super(FormMultiPage, self)._clear_all_widgets()
        self._pages__     = [ [],]
        self._active_page = 0
        self.switch_page(self._active_page, display=False)
    
    def switch_page(self, page, display=True):
        self._widgets__ = self._pages__[page]
        self._active_page = page
        self.editw = 0
        if display:
            self.display(clear=True)
    
    def add_page(self):
        self._pages__.append([])
        page_number   = len(self._pages__)-1
        self.nextrely = self.DEFAULT_NEXTRELY
        self.nextrelx = self.DEFAULT_X_OFFSET
        self.switch_page(page_number, display=False)
        return page_number
    
    def find_next_editable(self, *args):
        if not self.editw == len(self._widgets__):
            value_changed = False
            if not self.cycle_widgets:
                r = list(range(self.editw+1, len(self._widgets__)))
            else:
                r = list(range(self.editw+1, len(self._widgets__))) + list(range(0, self.editw))
            for n in r:
                if self._widgets__[n].editable and not self._widgets__[n].hidden: 
                    self.editw = n
                    value_changed = True
                    break
            if not value_changed:
                if self._active_page < len(self._pages__)-1:
                    self.switch_page(self._active_page + 1)
        self.display()
    
    def find_previous_editable(self, *args):
        if self.editw == 0:
            if self._active_page > 0:
                self.switch_page(self._active_page-1)
        
        if not self.editw == 0:     
            # remember that xrange does not return the 'last' value,
            # so go to -1, not 0! (fence post error in reverse)
            for n in range(self.editw-1, -1, -1 ):
                if self._widgets__[n].editable and not self._widgets__[n].hidden: 
                    self.editw = n
                    break
    
    