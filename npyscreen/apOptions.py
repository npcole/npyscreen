import weakref
import textwrap

from . import fmPopup

from . import wgtitlefield
from . import wgannotatetextbox
from . import wgmultiline
from . import wgselectone
from . import wgmultiselect
from . import wgeditmultiline
from . import wgcheckbox
from . import wgfilenamecombo
from . import wgdatecombo


class OptionListDisplayLine(wgannotatetextbox.AnnotateTextboxBase):
    ANNOTATE_WIDTH = 25   
    def getAnnotationAndColor(self):
        return (self.value.get_name_user(), 'LABEL')
    
    def display_value(self, vl):
        return vl.get_for_single_line_display()
        
class OptionListDisplay(wgmultiline.MultiLineAction):
    _contained_widgets = OptionListDisplayLine
    def actionHighlighted(self, act_on_this, key_press):
        rtn = act_on_this.change_option()
        self.display()
        return rtn
    
    def display_value(self, vl):
        return vl

class OptionChanger(fmPopup.ActionPopupWide):
    pass

    def on_ok(self,):
        self.OPTION_TO_CHANGE.set_from_widget_value(self.OPTION_WIDGET.value)

class OptionList(object):
    def __init__(self, ):
        self.options = []

class Option(object):
    def __init__(self, name, value=None, documentation=None, short_explanation=None):
        self.name = name
        self.set(value)
        self.documentation = documentation
        self.short_explanation = short_explanation
    
    def get(self,):
        return self.value
    
    def get_for_single_line_display(self):
        return repr(self.value)
    
    def set_from_widget_value(self, vl):
        self.set(vl)
    
    def set(self, value):
        self.value = value
    
    def get_real_name(self):
        # This might be for internal use
        return self.name
    
    def get_name_user(self):
        # You could do translation here.
        return self.name
    
    def _set_up_widget_values(self, option_form, main_option_widget):
        main_option_widget.value = self.value
    
    def change_option(self):
        option_changing_form = OptionChanger()
        option_changing_form.OPTION_TO_CHANGE = weakref.proxy(self)
        if self.documentation:
            explanation_widget = option_changing_form.add(wgmultiline.Pager, 
                                                        editable=False, value=None,
                                                        max_height=(option_changing_form.lines - 3) //2,
                                                        autowrap=True,
                                                        )
            option_changing_form.nextrely += 1
            explanation_widget.values = self.documentation
            
        
        option_widget = option_changing_form.add(self.WIDGET_TO_USE, name=self.get_name_user())
        option_changing_form.OPTION_WIDGET = option_widget
        self._set_up_widget_values(option_changing_form, option_widget)        
        option_changing_form.edit()
        
    

class OptionLimitedChoices(Option):
    def __init__(self, name, choices=None, *args, **keywords):
        super(OptionLimitedChoices, self).__init__(name, *args, **keywords)
        choices = choices or []
        self.setChoices(choices)
    
    def setChoices(self, choices):
        self.choices = choices
    
    def getChoices(self,):
        return self.choices
    
    def _set_up_widget_values(self, option_form, main_option_widget):
        main_option_widget.value  = []
        main_option_widget.values = self.getChoices()
        for x in range(len(main_option_widget.values)):
            if self.value and main_option_widget.values[x] in self.value:
                main_option_widget.value.append(x)
    
    def set_from_widget_value(self, vl):
        value = []
        for v in vl:
            value.append(self.choices[v])
        self.set(value)
        
class OptionFreeText(Option):
    WIDGET_TO_USE = wgtitlefield.TitleText

class OptionSingleChoice(OptionLimitedChoices):
    WIDGET_TO_USE = wgselectone.TitleSelectOne

class OptionMultiChoice(OptionLimitedChoices):
    WIDGET_TO_USE = wgmultiselect.TitleMultiSelect

class OptionMultiFreeText(Option):
    WIDGET_TO_USE = wgeditmultiline.MultiLineEdit

class OptionBoolean(Option):
    WIDGET_TO_USE = wgcheckbox.Checkbox

class OptionFilename(Option):
    WIDGET_TO_USE = wgfilenamecombo.FilenameCombo
    
class OptionDate(Option):
    WIDGET_TO_USE = wgdatecombo.DateCombo