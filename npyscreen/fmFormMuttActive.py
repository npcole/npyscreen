import weakref
import re
import curses
from . import fmFormMutt
from . import fmFormWithMenus
from . import npysNPSFilteredData
from . import wgtextbox

class ActionControllerSimple(object):
    def __init__(self, parent=None):
        try:
            self.parent = weakref.proxy(parent)
        except:
            self.parent = parent
        self._action_list = []
        self.create()
    
    def create(self):
        pass
    
    def add_action(self, ident, function, live):
        ident = re.compile(ident)
        self._action_list.append({'identifier': ident, 
                                  'function': function, 
                                  'live': live 
                                  })
    
    def process_command_live(self, command_line, control_widget_proxy):
        for a in self._action_list:
            if a['identifier'].match(command_line) and a['live']==True:
                a['function'](command_line, control_widget_proxy, live=True)
                
    def process_command_complete(self, command_line, control_widget_proxy):
        for a in self._action_list:
            if a['identifier'].match(command_line):
                a['function'](command_line, control_widget_proxy, live=False)

class TextCommandBox(wgtextbox.Textfield):
    def set_up_handlers(self):
        super(TextCommandBox, self).set_up_handlers()
        self.handlers.update({
                   curses.ascii.NL:     self.h_execute_command,
                   curses.ascii.CR:     self.h_execute_command,
        })
    
    def h_execute_command(self, *args, **keywords):
        self.parent.action_controller.process_command_complete(self.value, weakref.proxy(self))
        self.value = ''
        
    def when_value_edited(self):
        super(TextCommandBox, self).when_value_edited()
        if self.editing:
            self.parent.action_controller.process_command_live(self.value, weakref.proxy(self))
        else:
            self.parent.action_controller.process_command_complete(self.value, weakref.proxy(self))


class TextCommandBoxTraditional(TextCommandBox):
    # EXPERIMENTAL
    # NOT READY FOR ACTUAL USE.
    # BUT WILL PASS INPUT TO A LINKED WIDGET - THE LINKED WIDGET
    # WILL NEED TO BE ALTERED TO LOOK AS IF IT IS BEING EDITED TOO.
    BEGINNING_OF_COMMAND_LINE_CHARS = ":/"
    def __init__(self, *args, **keywords):
        super(TextCommandBoxTraditional, self).__init__(*args, **keywords)
        self.linked_widget = None
    
    def handle_input(self, inputch):
        try:
            inputchstr = chr(inputch)
        except:
            inputchstr = False
        if not self.linked_widget:
            return super(TextCommandBoxTraditional, self).handle_input(inputch)
        
        if inputchstr and (self.value == '' or self.value == None):
            if inputchstr in self.BEGINNING_OF_COMMAND_LINE_CHARS:
                return super(TextCommandBoxTraditional, self).handle_input(inputch)
            
        if self.value:
            return super(TextCommandBoxTraditional, self).handle_input(inputch)
        
        rtn = self.linked_widget.handle_input(inputch)
        self.linked_widget.update()
        return rtn

class FormMuttActive(fmFormMutt.FormMutt):
    DATA_CONTROLER    = npysNPSFilteredData.NPSFilteredDataList
    ACTION_CONTROLLER  = ActionControllerSimple
    COMMAND_WIDGET_CLASS = TextCommandBox
    def __init__(self, *args, **keywords):
        super(FormMuttActive, self).__init__(*args, **keywords)
        self.set_value(self.DATA_CONTROLER())
        self.action_controller = self.ACTION_CONTROLLER(parent=self)

class FormMuttActiveWithMenus(FormMuttActive, fmFormWithMenus.FormBaseNewWithMenus):
    def __init__(self, *args, **keywords):
        super(FormMuttActiveWithMenus, self).__init__(*args, **keywords)
        self.initialize_menus()
        
        
class FormMuttActiveTraditional(fmFormMutt.FormMutt):
    DATA_CONTROLER    = npysNPSFilteredData.NPSFilteredDataList
    ACTION_CONTROLLER  = ActionControllerSimple
    COMMAND_WIDGET_CLASS = TextCommandBoxTraditional
    def __init__(self, *args, **keywords):
        super(FormMuttActiveTraditional, self).__init__(*args, **keywords)
        self.set_value(self.DATA_CONTROLER())
        self.action_controller        = self.ACTION_CONTROLLER(parent=self)
        self.wCommand.linked_widget   = self.wMain
        self.wMain.editable           = False
        self.wMain.always_show_cursor = True

class FormMuttActiveTraditionalWithMenus(FormMuttActiveTraditional, 
 fmFormWithMenus.FormBaseNewWithMenus):
    def __init__(self, *args, **keywords):
        super(FormMuttActiveTraditionalWithMenus, self).__init__(*args, **keywords)
        self.initialize_menus()




        