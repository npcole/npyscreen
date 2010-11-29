from . import fmFormMutt
from . import npysNPSFilteredData
from . import wgtextbox

class ActionControllerSimple(object):
    def __init__(self):
        self._action_list = []
    
    def add_action(self, ident, function, live):
        self._action_list.append({'identifier': ident, 
                                  'function': function, 
                                  'live': live 
                                  })
    
    def process_command_live(self, command_line):
        for a in self._action_list:
            if command_line.startswith(a['identifier']) and a['live']:
                a[function](command_line)
                
    def process_command_complete(self, command_line, live=True):
        for a in self._action_list:
            if command_line.startswith(a['identifier']):
                a[function](command_line, live=False)

class TextCommandBox(wgtextbox.Textfield):
    pass

class FormMuttActive(fmFormMutt.FormMutt):
    DATA_CONTROLER    = npysNPSFilteredData.NPSFilteredDataList
    ACTION_CONTROLER  = ActionControllerSimple
    def __init__(self, *args, **keywords):
        super(FormMuttActive, self).__init__(*args, **keywords)
        self.value = self.DATA_CONTROLER()
        self.action_controller = self.ACTION_CONTROLER()
        
    

class FormMuttActiveWithMenus(FormMuttActive):
    def __init__(self, *args, **keywords):
        super(FormMuttActiveWithMenus, self).__init__(*args, **keywords)
        self.initialize_menus()
        