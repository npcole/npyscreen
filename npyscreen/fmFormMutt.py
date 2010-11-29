#/usr/bin/env python
import curses
from . import fmForm
from . import fmFormWithMenus
from . import wgtextbox
from . import wgmultiline
#import grid
#import editmultiline


class FormMutt(fmForm.FormBaseNew):
    BLANK_LINES_BASE     = 0
    BLANK_COLUMNS_RIGHT  = 0
    DEFAULT_X_OFFSET = 2
    FRAMED = False
    MAIN_WIDGET_CLASS   = wgmultiline.MultiLine
    STATUS_WIDGET_CLASS = wgtextbox.Textfield
    COMMAND_WIDGET_CLASS= wgtextbox.Textfield
    #MAIN_WIDGET_CLASS = grid.SimpleGrid
    #MAIN_WIDGET_CLASS = editmultiline.MultiLineEdit
    def __init__(self, cycle_widgets = True, *args, **keywords):
        super(FormMutt, self).__init__(cycle_widgets=cycle_widgets, *args, **keywords)
    
    
    def draw_form(self):
        MAXY, MAXX = self.lines, self.columns #self.curses_pad.getmaxyx()
        self.curses_pad.hline(0, 0, curses.ACS_HLINE, MAXX-1)  
        self.curses_pad.hline(MAXY-2, 0, curses.ACS_HLINE, MAXX-1)  

    def create(self):
        MAXY, MAXX    = self.lines, self.columns
        self.wStatus1 = self.add(self.__class__.STATUS_WIDGET_CLASS,  rely=0, relx=0,      editable=False,  )
        self.wMain    = self.add(self.__class__.MAIN_WIDGET_CLASS,    rely=1,  relx=0,     max_height = -2, )
        self.wStatus2 = self.add(self.__class__.STATUS_WIDGET_CLASS,  rely=MAXY-2, relx=0, editable=False,  )
        self.wCommand = self.add(self.__class__.COMMAND_WIDGET_CLASS, rely = MAXY-1, relx=0,)
        self.wStatus1.important = True
        self.wStatus2.important = True
        self.nextrely = 2

    def h_display(self, input):
        super(FormMutt, self).h_display(input)
        self.wMain.display()

class FormMuttWithMenus(FormMutt, fmFormWithMenus.FormBaseNewWithMenus):
    def __init__(self, *args, **keywords):
        super(FormMuttWithMenus, self).__init__(*args, **keywords)
        self.initialize_menus()
