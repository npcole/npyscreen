import weakref
import re
import curses
from . import fmFormMutt
from . import npysNPSFilteredData
from . import wgtextbox

class ActionControllerSimple(object):
    def __init__(self, parent=None):
        try:
            self.parent = weakref.proxy(parent)
        except:
            self.parent = parent
        self._action_list = []
    
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

class FormMuttActive(fmFormMutt.FormMutt):
    DATA_CONTROLER    = npysNPSFilteredData.NPSFilteredDataList
    ACTION_CONTROLLER  = ActionControllerSimple
    COMMAND_WIDGET_CLASS = TextCommandBox
    def __init__(self, *args, **keywords):
        super(FormMuttActive, self).__init__(*args, **keywords)
        self.set_value(self.DATA_CONTROLER())
        self.action_controller = self.ACTION_CONTROLLER(parent=self)
        
    

class FormMuttActiveWithMenus(FormMuttActive):
    def __init__(self, *args, **keywords):
        super(FormMuttActiveWithMenus, self).__init__(*args, **keywords)
        self.initialize_menus()
        